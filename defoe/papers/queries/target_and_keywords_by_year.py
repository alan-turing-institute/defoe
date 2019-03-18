"""
Counts number of articles containing both a target word and one or
more keywords and groups by year.

Words in articles, target words and keywords can be normalized,
normalized and stemmed, or normalized and lemmatized (default).
"""

import os.path
from operator import add
import yaml

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.papers.query_utils import get_article_keywords


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of articles containing both a target word and one or
    more keywords and groups by year.

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
            {
              "target_word": <WORD>,
              "words": [<WORD>, <WORD>, ...],
              "count": <COUNT>
            },
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
        keywords = [query_utils.preprocess_word(word, preprocess_type)
                    for word in list(f)]

    target_word = keywords[0]
    keywords = keywords[1:]

    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article)
                       for article in issue.articles])
    # [(year, article), ...]
    target_articles = articles.filter(
        lambda year_article: article_contains_word(
            year_article[1], target_word, preprocess_type))
    # [((year, [word, word, ...]), 1), ...]
    words = target_articles.map(
        lambda year_article: (
            (year_article[0],
             get_article_keywords(year_article[1],
                                  keywords,
                                  preprocess_type)),
            1))
    # [((year, [word, word, ...]), 1), ...]
    match_words = words.filter(
        lambda yearword_count: len(yearword_count[0][1]) > 0)
    # [((year, "target_word, word, word, ..."), 1), ...]
    # Convert word list to string so can serve as a key.
    multi_words = match_words.map(
        lambda yearword_count: (
            (yearword_count[0][0],
             ",".join(yearword_count[0][1])),
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
    # list of words is restored from string of words.
    result = multi_words \
        .reduceByKey(add) \
        .map(lambda yearword_count:
             (yearword_count[0][0],
              (yearword_count[0][1],
               yearword_count[1]))) \
        .groupByKey() \
        .map(lambda year_wordcount:
             (year_wordcount[0],
              word_article_count_list_to_dict(target_word,
                                              year_wordcount[1])))\
        .collect()
    return result


def word_article_count_list_to_dict(target_word, word_counts):
    """
    Converts list of tuples of words and counts of articles these
    occur in into list of dictionaries of target word, lists of words
    and counts.

    List is of form:

       [("word, word, ...", count), ...]

    Dictionary is of form:

        {
            "target": <WORD>,
            "words": [<WORD>, <WORD>, ...],
            "count": <COUNT>
        }

    :param target_word: target word
    :type target_word: str or unicode
    :param word_counts: words and counts
    :type word_counts: list(tuple(list(str or unicode), int))
    :return: dict
    :rtype: dict
    """
    result = []
    for word_count in word_counts:
        result.append({"target_word": target_word,
                       "words": word_count[0].split(","),
                       "count": word_count[1]})
    return result
