"""
Counts number of times that each keyword appears for every article
that has a target word in it.

Words in articles, target words and keywords can be normalized,
normalized and stemmed, or normalized and lemmatized (default).
"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.query_utils import PreprocessWordType


PREPROCESS_TYPE = PreprocessWordType.LEMMATIZE
""" Default word pre-processing type """


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of times that each keyword appears for every article
    that has a target word in it.

    Words in articles, target words and keywords can be normalized,
    normalized and stemmed, or normalized and lemmatized (default).

    config_file must be the path to a configuration file with a target
    word and a list of one or more keywords to search for, one per
    line.

    Returns result of form:

        {
            <YEAR>:
            [
                [<WORD>, <NUM_WORDS>],
                [<WORD>, <NUM_WORDS>],
                ...
            ],
            <YEAR>:
            ...
        }

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
        keywords = [query_utils.preprocess_word(
            word, PREPROCESS_TYPE) for word in list(f)]

    target_word = keywords[0]
    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article)
                       for article in issue.articles])
    # [(year, article), ...]
    target_articles = articles.filter(
        lambda year_article: article_contains_word(
            year_article[1], target_word, PREPROCESS_TYPE))

    # [((year, word), 1), ...]
    words = target_articles.flatMap(
        lambda target_article: [
            ((target_article[0],
              query_utils.preprocess_word(word, PREPROCESS_TYPE)), 1)
            for word in target_article[1].words
        ])

    # [((year, word), 1), ...]
    matching_words = words.filter(
        lambda yearword_count: yearword_count[0][1] in keywords)
    # [((year, word), num_words), ...]
    # =>
    # [(year, (word, num_words)), ...]
    # =>
    # [(year, [word, num_words]), ...]
    result = matching_words \
        .reduceByKey(add) \
        .map(lambda yearword_count:
             (yearword_count[0][0],
              (yearword_count[0][1], yearword_count[1]))) \
        .groupByKey() \
        .map(lambda year_wordcount:
             (year_wordcount[0], list(year_wordcount[1]))) \
        .collect()
    return result
