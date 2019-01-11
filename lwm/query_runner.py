"""
Run Spark text analysis job.

An optional <NUM_CORES> argument can be given, specifying the number
of cores Spark should use. If omitted, defaults to 1.

The following files are read.

job.json:

* Job configuration.

    {
        "model": "books"|"papers"
    }

* "model" specifies whether "book" or "paper" model is to be used. The
  model determines the modules loaded. These are assumed to be

  - "lwm.<MODEL>.sparkrods", which must have a "get_streams" function.
  - "lwm.<MODEL>.query", which must have a "do_query" function.

data.txt:

* URLs or file paths, specifying data to be analysed, one per line.

query.dat:

* Query-specific configuration (optional, depends on the query module
  implementation.

Results are placed in a YAML file, results.yml.
"""

import importlib
import json
import sys
import yaml

from pyspark import SparkContext, SparkConf


def main():
    """
    Run Spark text analysis job.
    """
    job_config_file = "job.json"
    models = ["books", "papers"]
    num_cores = 1
    data_file = "data.txt"
    query_config_file = "query.dat"
    results_file = "results.yml"

    if len(sys.argv) > 1:
        num_cores = sys.argv[1]

    with open(job_config_file, "r") as f:
        job_config = json.load(f)
    assert "model" in job_config, "Missing model from " + job_config_file
    model_name = job_config["model"]
    assert model_name in models, ("'model' should be one of " + str(models))

    sparkrods = importlib.import_module("lwm." + model_name + ".sparkrods")
    query = importlib.import_module("lwm." + model_name + ".query")
    get_streams = sparkrods.get_streams
    do_query = query.do_query

    conf = SparkConf()
    conf.setAppName(model_name)
    conf.set("spark.cores.max", num_cores)

    context = SparkContext(conf=conf)
    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)
    data = get_streams(context, num_cores, source=data_file)
    results = do_query(data, query_config_file, log)

    with open(results_file, "w") as results_file:
        results_file.write(yaml.safe_dump(dict(results)))


if __name__ == "__main__":
    main()
