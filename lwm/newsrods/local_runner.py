"""
A runner to run the analysis directly on remotes using
"""

from os import environ

from newsrods.query import do_query
from newsrods.ucl_sparkrods import get_streams

from pyspark import SparkContext

import yaml


def main():
    """
    Link the file loading with the query
    """

    context = SparkContext(appName='iNewspaperRods')

    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)

    issues = get_streams(context, username=environ['USER'], source='files.txt')
    results = do_query(issues, 'input.1.data', log)

    with open('result.1.yml', 'w') as result_file:
        result_file.write(yaml.safe_dump(dict(results)))


if __name__ == '__main__':
    main()
