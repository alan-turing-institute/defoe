"""
Run Spark several text queries jobs.

    usage: run_queries.py [-h] [-n [NUM_CORES]]  [-e [ERRORS_FILE]]
                      data_file model_name -l query_list [query_config_file]

    Run Spark text analysis job

    positional arguments:
      data_file             Data file listing data files to query
      model_name            Data model to which data files conform:
      ['books', 'papers', 'fmp','nzpp', 'generic_xml', 'nls', 'hdfs', 'psql', 'es']
      query_list            A file with the queries to run. For each query
                            we have to indicate: query_module [query_configuration_file] [-r results_file]
       Example:
       defoe.nls.queries.normalize -r results.txt
       defoe.nls.queries.keysearch_by_year queries/sport.yml -r results_sc_sports


    optional arguments:
      -h, --help            show this help message and exit
      -n [NUM_CORES], --num_cores [NUM_CORES]
                            Number of cores
      -e [ERRORS_FILE], --errors_file [ERRORS_FILE]
                            Errors file

* data_file: lists either URLs or paths to files on the file system.
* model_name: text model to be used. The model determines the modules
  loaded. Given a "model_name" value of "<MODEL_NAME>" then a module
  "defoe.<MODEL_NAME>.setup" must exist and support a function:

    tuple(Object | str or unicode, str or unicode)
    filename_to_object(str or unicode: filename)

  - tuple(Object, None) is returned where Object is an instance of the
  - object model representing the data, if the file was successfully
  - read and parsed into an object
  - tuple(str or unicode, filename) is returned with the filename and
  - an error message, if the file was not successfully read and parsed
  - into an object
* query_name: name of Python module implementing the query to run
  e.g. "defoe.alto.queries.find_words_group_by_word" or
  "defoe.papers.queries.articles_containing_words". The query must be
  compatible with the chosen model in "model_name". The module
  must support a function

    list do_query(pyspark.rdd.PipelinedRDD rdd,
                  str|unicode config_file,
                  py4j.java_gateway.JavaObject logger)

* "query_config_file": query-specific configuration file. This is
  optional and depends on the chosen query module above.
* results_file": name of file to hold query results in YAML
  format. Default: "results_NUM_QUERY.yml".
"""

from argparse import ArgumentParser
import importlib
import os.path
import yaml

from pyspark import SparkContext, SparkConf

from defoe.spark_utils import files_to_rdd


def main():
    """
    Run Spark text analysis job.
    """
    root_module = "defoe"
    setup_module = "setup"
    models = ["books", "papers", "fmp", "nzpp", "generic_xml", "nls", "hdfs", "psql", "es"]

    parser = ArgumentParser(description="Run Spark text analysis job")
    parser.add_argument("data_file",
                        help="Data file listing data files to query")
    parser.add_argument("model_name",
                        help="Data model to which data files conform: " +
                        str(models))
    parser.add_argument("-l",
                        "--queries_list",
                        nargs="?",
                        help="Queries list file")
    parser.add_argument("-n",
                        "--num_cores",
                        nargs="?",
                        default=1,
                        help="Number of cores")
    parser.add_argument("-e",
                        "--errors_file",
                        nargs="?",
                        default="errors.yml",
                        help="Errors file")

    args = parser.parse_args()
    model_name = args.model_name
    queries_list = args.queries_list
    data_file = args.data_file
    num_cores = args.num_cores
    errors_file = args.errors_file

    

    assert model_name in models, ("'model' must be one of " + str(models))

    # Dynamically load model and query modules.
    setup = importlib.import_module(root_module +
                                    "." +
                                    model_name +
                                    "." +
                                    setup_module)


    filename_to_object = setup.filename_to_object
    
    # Configure Spark.
    conf = SparkConf()
    conf.setAppName(model_name)
    conf.set("spark.cores.max", num_cores)
    
    # Submit job.
    context = SparkContext(conf=conf)
    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)  # pylint: disable=protected-access
    
    if (model_name!= "hdfs") and (model_name!= "psql") and (model_name!= "es"):
        # [filename,...]
        rdd_filenames = files_to_rdd(context, num_cores, data_file=data_file)
        # [(object, None)|(filename, error_message), ...]
        data = rdd_filenames.map(
             lambda filename: filename_to_object(filename))

        # [object, ...]
        ok_data = data \
            .filter(lambda obj_file_err: obj_file_err[1] is None) \
            .map(lambda obj_file_err: obj_file_err[0])
        # [(filename, error_message), ...]
        error_data = data \
            .filter(lambda obj_file_err: obj_file_err[1] is not None) \
            .map(lambda obj_file_err: (obj_file_err[0], obj_file_err[1]))
        # Collect and record problematic files before attempting query.
        errors = error_data.collect()
        errors = list(errors)
        if errors:
            with open(errors_file, "w") as f:
                 f.write(yaml.safe_dump(list(errors)))
    
    else: 
        ok_data=filename_to_object(data_file, context)
 

    
   # Lets open the queries list and run each of them: 
    f = open(queries_list, "r")
    queries = f.readlines()
    f.close()

    num_query=0
    for query in queries:
        query_l=query.rstrip()
        arguments=query_l.split(" ")
        query_name = arguments[0]
        # Default Values for results and config_file:
        query_config_file = None
        results_file = "results_"+str(num_query)+".yml"
  
        if arguments[1]:
            if arguments[1] != "-r":
                 query_config_file = arguments[1]
                 if arguments[2]:
                     results_file = arguments[3]
            else :
                results_file = arguments[2]
              
        for f in [results_file, errors_file]:
            if os.path.exists(f):
                os.remove(f)
        
        query = importlib.import_module(query_name)
        do_query = query.do_query
        results = do_query(ok_data, query_config_file, log, context)
        if results!="0":
            with open(results_file, "w") as f:
                 f.write(yaml.safe_dump(dict(results)))
        num_query+=1


if __name__ == "__main__":
    main()
