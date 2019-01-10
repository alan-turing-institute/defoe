"""
A module to get all of the different OCR qualities for each year
"""

from operator import concat


def do_query(issues, _input, _log):
    """
    Get the list of OCR qualities for each year
    """

    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year,
                                              [article.quality]) for
                                             article in issue.articles]) \
        .reduceByKey(concat) \
        .collect()
    return articles
