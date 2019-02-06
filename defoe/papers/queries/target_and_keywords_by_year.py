"""
Counts number of articles containing both a target word and more
keywords and groups by year.
"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.papers.query_utils import get_keywords_in_article
from defoe.papers.query_utils import word_article_count_list_to_dict


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of articles containing both a target word and more
    keywords and groups by year.

    config_file must be the path to a configuration file with a target
    word and a list of one or more keywords to search for, one per
    line.

    Target word, keywords and words in documents are normalized, by
    removing all non-'a-z|A-Z' characters.

    Returns result of form:

        <YEAR>:
        - {
            "words": "<TARGET_WORD>, <WORD>, ...",
            "count": <COUNT>
          }
        - {
            "words": "<TARGET_WORD>, <WORD>, ...",
            "count": <COUNT>
          }
        - ...
        <YEAR>:
        ...

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped by year
    :rtype: dict
    """
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.normalize(word) for word in list(f)]

    target_word = keywords[0]
    keywords = keywords[1:]

    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article)
                       for article in issue.articles])

    # [(year, article), ...]
    articles = articles.filter(
        lambda year_article: article_contains_word(
            year_article[1], target_word))

    # [((year, [word, word, ...]), 1), ...]
    words = articles.map(
        lambda year_article: (
            (year_article[0],
             get_keywords_in_article(year_article[1], keywords)),
            1))
    # [((year, [word, word, ...]), 1), ...]
    match_words = words.filter(
        lambda yearword_count: len(yearword_count[0][1]) > 1)
    # [((year, "word, word, ..."), 1), ...]
    multi_words = match_words.map(
        lambda yearword_count: (
            (yearword_count[0][0],
             str(yearword_count[0][1])),
            yearword_count[1]))
    # [((year, "word, word, ..."), 1), ...]
    # =>
    # [((year, "word, word, ..."), count), ...]
    # =>
    # [((year, ("word, word, ...", count)), ...]
    # =>
    # [((year, [{"words": "word, word, ...",
    #            "count": count}, ...],
    #          ...]
    result = multi_words \
        .reduceByKey(add) \
        .map(lambda yearword_count:
             (yearword_count[0][0],
              (yearword_count[0][1],
               yearword_count[1]))) \
        .groupByKey() \
        .map(lambda year_wordcount:
             (year_wordcount[0],
              word_article_count_list_to_dict(year_wordcount[1])))\
        .collect()
    return result
