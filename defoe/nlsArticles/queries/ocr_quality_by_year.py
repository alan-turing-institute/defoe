"""
Gets measure of OCR quality for each page and groups by year.
"""

from operator import concat
from defoe.nls.query_utils import calculate_words_within_dictionary

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Gets measure of OCR quality (PC), and calculates the number of words found in a dictionary for each page and groups by year.

    Returns result of form:

        {
          <YEAR>: [<QUALITY>, ...],
          ...
        }

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: OCR quality and percentage of words found  of article grouped by year
    :rtype: dict
    """
    # [(year, document), ...]
    documents = archives.flatMap(
        lambda archive: [(document.year, document) for document in list(archive)])

    # [(year, [quality]), ...]
    qualities = documents.flatMap(
        lambda document: [(document[0], [page.pc, calculate_words_within_dictionary(page)]) for page in document[1]])
    result = qualities \
        .groupByKey() \
        .map(lambda year_q:
             (year_q[0], list(year_q[1]))) \
        .collect()
    return result
