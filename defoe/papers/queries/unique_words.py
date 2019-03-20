"""
Finds every unique word and its frequency.
"""

from operator import add
import os.path
import yaml

from defoe import query_utils


def do_query(issues, config_file=None, logger=None):
    """
    Finds every unique word and its frequency.

    config_file can be the path to a configuration file with a
    threshold, the minimum number of occurrences of the word for the
    word to be counted. This file, if provided, must be of form:

        threshold: <COUNT>

    where <COUNT> is >= 1.

    If no configuration file is provided then a threshold of 1 is
    assumed.

    Words in documents are normalized, by removing all non-'a-z|A-Z'
    characters.

    Returns result of form:

        {
          <WORD>: <COUNT>,
          ...
        }

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (optional)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of issues and words
    :rtype: dict
    """
    threshold = 1
    if config_file is not None and\
       os.path.exists(config_file) and\
       os.path.isfile(config_file):
        with open(config_file, "r") as f:
            config = yaml.load(f)
        value = config["threshold"]
        threshold = max(threshold, value)

    # [article, article, ...]
    articles = issues.flatMap(lambda issue:
                              [article for article in issue.articles])

    # [(word, 1), (word, 1), ...]
    words = articles.flatMap(lambda article:
                             [(query_utils.normalize(word), 1) for word in article.words])

    # [(word, 1), (word, 1), ...]
    # =>
    # [(word, count), (word, count), ...]
    word_counts = words. \
        reduceByKey(add). \
        filter(lambda word_year: word_year[1] > threshold). \
        collect()
    return word_counts
