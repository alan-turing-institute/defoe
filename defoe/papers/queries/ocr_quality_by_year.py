"""
Gets measure of OCR quality for each article and groups by year.
"""

from operator import concat


def do_query(issues, config_file=None, logger=None):
    """
    Gets measure of OCR quality for each article and groups by year.

    Returns result of form:

        {
          <YEAR>: [<QUALITY>, ...],
          ...
        }

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: OCR quality of article grouped by year
    :rtype: dict
    """
    # [(year, [quality]), ...]
    qualities = issues.flatMap(
        lambda issue: [(issue.date.year, [article.quality]) for article in issue.articles])

    result = qualities \
        .reduceByKey(concat) \
        .collect()
    return result
