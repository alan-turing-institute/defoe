"""
Gets measure of OCR quality for each page and groups by year.
"""

from operator import concat


def do_query(archives, config_file=None, logger=None):
    """
    Gets measure of OCR quality for each page and groups by year.

    Returns result of form:

        {
          <YEAR>: [<QUALITY>, ...],
          ...
        }

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: OCR quality of article grouped by year
    :rtype: dict
    """
    # [(year, document), ...]
    documents = archives.flatMap(
        lambda archive: [(document.year, document) for document in list(archive)])

    # [(year, [quality]), ...]
    qualities = documents.flatMap(
        lambda document: [(document[0], [page.pc]) for page in document[1]])
    result = qualities \
        .reduceByKey(concat) \
        .collect()
    return result
