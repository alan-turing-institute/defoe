"""
Counts total number of issues.
"""


def do_query(issues, config_file=None, logger=None):
    """
    Iterate through issues and count total number of issues.
    Returns result of form:

        {"num_issues": num_issues}

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of issues
    :rtype: dict
    """
    num_issues = issues.count()
    return {"num_issues": num_issues}
