"""
This module counts the number of articles that per year that contain
the word "prof", "prof." or "professor".
"""

from operator import add
import re


def do_query(issues, interesting_words_file, _log):
    """
    Get number of articles which contain the word "prof", "prof."
    or "professor".
    """
    words = ["prof", "prof.", "professor"]
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year, article) for
                                             article in issue.articles])
    # Add 1 record for each word that appears in each article in each year
    interest = articles.flatMap(lambda (year, article):
                                [((year, word), 1) for word in
                                 words if word in (w.lower() for w in article.words)])
    # Add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(add) \
        .map(lambda (year_word, count): (year_word[0],
                                         (year_word[1].replace(r'\b', ''),
                                          count))) \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    return interesting_by_year
