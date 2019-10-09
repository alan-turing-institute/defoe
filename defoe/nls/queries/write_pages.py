"""
Counts number of occurrences of keywords or keysentences and groups by year.
"""

from operator import add

from defoe.query_utils import PreprocessWordType
from defoe.nls.query_utils import get_page_as_string

import yaml, os

def do_query(archives, config_file=None, logger=None):
    """
    Counts number of occurrences of keywords or keysentences and groups by year.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords/keysentences and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <YEAR>:
          [
            [<SENTENCE|WORD>, <NUM_SENTENCES|WORDS>],
            ...
          ],
          <YEAR>:
          ...
        }

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped by year
    :rtype: dict
    """
    # [(year, title, place, publisher, date, document), ...]
    preprocess_type=4
    documents = archives.flatMap(
        lambda archive: [(document.year, document.title, document.place, document.publisher, document.date, document) for document in list(archive)])
    # [(year, title, place, publisher, date, page_string)
    pages = documents.flatMap(
        lambda year_document: [(year_document[0],year_document[1], year_document[2], year_document[3], year_document[4], 
                                    get_page_as_string(page, preprocess_type)) 
                                       for page in year_document[5]])

    pages.saveAsTextFile("hdfs:///user/at003/rosa/text6.txt")
    return "0"
