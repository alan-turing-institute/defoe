"""
Gets page and the average of all words confidences for each page and groups by year.

"""

from operator import concat, add
from defoe.nls.query_utils import calculate_words_confidence_average

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Gets measure of Page Confidence (PC) and caculate the avergage of all words confidences (WC) per page. 

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
    :return: Page confidence and the average of words confidences  of pages grouped by year
    :rtype: dict
    """
    # [(year, document), ...]
    documents = archives.flatMap(
        lambda archive: [(document.year, document) for document in list(archive)])

    # [(year, [page_confidence, average_words_confidence ]), ...]
    qualities = documents.flatMap(
        lambda document: [(document[0], [page.pc, calculate_words_confidence_average(page)]) for page in document[1]])
    result = qualities \
        .groupByKey() \
        .map(lambda year_q:
             (year_q[0], list(year_q[1]))) \
        .collect()
    return result
