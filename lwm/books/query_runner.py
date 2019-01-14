"""
Run Spark text analysis job.

An optional <NUM_CORES> argument can be given, specifying
the number of cores Spark should use. If omitted, defaults to 1.

The following files are read:

* data.txt: URLs or file paths, for data to be analysed (mandatory)
* query.dat: query-specific configuration (optional)

Results are placed in a YAML file, results.yml.
"""

import sys
import yaml

from pyspark import SparkContext, SparkConf

from lwm.books.sparkrods import get_streams
from lwm.books.query import do_query


def main():
    """
    Run Spark text analysis job.
    """
    num_cores = 1
    if len(sys.argv) > 1:
        num_cores = sys.argv[1]

    conf = SparkConf()
    conf.setAppName("Books")
    conf.set("spark.cores.max", num_cores)

    context = SparkContext(conf=conf)
    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)
    archives = get_streams(context, num_cores, source="data.txt")
    results = do_query(archives, 'query.dat', log)

    with open('result.yml', 'w') as result_file:
        result_file.write(yaml.safe_dump(dict(results)))


if __name__ == "__main__":
    main()
