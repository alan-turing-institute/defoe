"""
Run Spark text query job.

    usage: run_query.py [-h] [-n [NUM_CORES]] [-r [RESULTS_FILE]]
                      data_file model_name query_name [query_config_file]

    Run Spark text analysis job

    positional arguments:
      data_file             Data file listing data files to query
      model_name            Data model to which data files conform:
      ['books',
                            'papers']
      query_name            Query module name
      query_config_file     Query-specific configuration file

    optional arguments:
      -h, --help            show this help message and exit
      -n [NUM_CORES], --num_cores [NUM_CORES]
                            Number of cores
      -r [RESULTS_FILE], --results_file [RESULTS_FILE]
                            Query results file

* data_file: lists either URLs or file paths which are the files over
  which the query is to be run, one per line. Either URLs or file
  paths should be exclusively used, not both.
* model_name: specifies which text model is to be used. The model
  determines the modules loaded. These are assumed to be:
  - "defoe.<MODEL_NAME>.sparkrods", which must have a
  "filenames_to_objects" function.
* query_name: name of Python module implementing the query to run
  e.g. "defoe.alto.queries.find_words_group_by_word" or
  "defoe.papers.queries.articles_containing_words". The query must
  be compatible with the chosen model.
* "query_config_file": query-specific configuration. This is optional
  and depends on the query implementation.
* results_file": file to hold query results in YAML format.
  Default: "results.yml".
"""

from argparse import ArgumentParser
import importlib
import yaml

from pyspark import SparkContext, SparkConf

from defoe.file_utils import files_to_rdd


def main():
    """
    Run Spark text analysis job.
    """
    root_module = "defoe"
    setup_module = "setup"
    models = ["books", "papers"]

    parser = ArgumentParser(description="Run Spark text analysis job")
    parser.add_argument("data_file",
                        help="Data file listing data files to query")
    parser.add_argument("model_name",
                        help="Data model to which data files conform: " +
                        str(models))
    parser.add_argument("query_name",
                        help="Query module name")
    parser.add_argument("query_config_file",
                        nargs="?",
                        default=None,
                        help="Query-specific configuration file")
    parser.add_argument("-n",
                        "--num_cores",
                        nargs="?",
                        default=1,
                        help="Number of cores")
    parser.add_argument("-r",
                        "--results_file",
                        nargs="?",
                        default="results.yml",
                        help="Query results file")

    args = parser.parse_args()
    model_name = args.model_name
    query_name = args.query_name
    data_file = args.data_file
    num_cores = args.num_cores
    query_config_file = args.query_config_file
    results_file = args.results_file

    assert model_name in models, ("'model' must be one of " + str(models))

    # Dynamically load model and query modules.
    setup = importlib.import_module(root_module +
                                    "." +
                                    model_name +
                                    "." +
                                    setup_module)
    query = importlib.import_module(query_name)
    filenames_to_objects = setup.filenames_to_objects
    do_query = query.do_query

    # Configure Spark.
    conf = SparkConf()
    conf.setAppName(model_name)
    conf.set("spark.cores.max", num_cores)

    # Submit job.
    context = SparkContext(conf=conf)
    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)
    rdd_filenames = files_to_rdd(context, num_cores, data_file=data_file)
    data = filenames_to_objects(rdd_filenames)
    results = do_query(data, query_config_file, log)

    # Write results.
    with open(results_file, "w") as results_file:
        results_file.write(yaml.safe_dump(dict(results)))


if __name__ == "__main__":
    main()
