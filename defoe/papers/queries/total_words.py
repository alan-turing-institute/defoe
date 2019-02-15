"""
Counts total number of words.
"""

from operator import add


def do_query(issues, config_file=None, logger=None):
    """
    Iterate through issues and count total number of issues
    and total number of words.

    Returns result of form:

        {
          "num_issues": num_issues,
          "num_words": num_words
        }

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of issues and words
    :rtype: dict
    """
    # [article, article, ...]
    articles = issues.flatMap(lambda issue:
                              [article for article in issue.articles])
    # [num_words, num_words, ...]
    num_words = articles.map(lambda article: len(list(article.words)))
    result = [issues.count(), num_words.reduce(add)]
    return {"num_issues": result[0],
            "num_words": result[1]}
