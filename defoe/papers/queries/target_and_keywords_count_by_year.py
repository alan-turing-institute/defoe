"""
Counts number of times that each keyword appears for every article
that has a target word in it.

Words in articles, target words and keywords can be normalized,
normalized and stemmed, or normalized and lemmatized (default).
"""

import os.path
from operator import add
import yaml

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of times that each keyword appears for every article
    that has a target word in it.

    Words in articles, target words and keywords can be normalized,
    normalized and stemmed, or normalized and lemmatized (default).

    config_file must be the path to a configuration file of form:

        preprocess: none|normalize|stem|lemmatize # Optional
        data: <DATA_FILE>

    <DATA_FILE> must be the path to a plain-text data file with a list
    of keywords to search for, one per line. The first word is assumed
    to be the target word. If <DATA_FILE> is a relative path then it
    is assumed to be relative to the directory in which config_file
    resides.

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
    with open(config_file, "r") as f:
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    keywords = []
    with open(data_file, 'r') as f:
        keywords = [query_utils.preprocess_word(
            word, preprocess_type) for word in list(f)]

    target_word = keywords[0]
    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article)
                       for article in issue.articles])
    # [(year, article), ...]
    target_articles = articles.filter(
        lambda year_article: article_contains_word(
            year_article[1], target_word, preprocess_type))

    # [((year, word), 1), ...]
    words = target_articles.flatMap(
        lambda target_article: [
            ((target_article[0],
              query_utils.preprocess_word(word, preprocess_type)), 1)
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
