'''
A runner to run the analysis directly on remotes using
'''

import os

from newsrods.query import do_query
from newsrods.ucl_sparkrods import get_streams

from pyspark import SparkContext

from yaml import safe_dump


def main():
    """
    Link the file loading with the query
    """

    context = SparkContext(appName='iNewspaperRods')

    log = context._jvm.org.apache.log4j.LogManager.getLogger(__name__)

    issues = get_streams(context,
                         os.environ['USER'],
                         source='files.{}.txt'
                         .format(os.environ['SGE_TASK_ID']))
    results = do_query(issues, 'input.1.data', log)

    with open('result.{}.yml'.
              format(os.environ['SGE_TASK_ID']), 'w') as result_file:
        result_file.write(safe_dump(dict(results)))


if __name__ == '__main__':
    main()
