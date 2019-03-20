"""
Counts number of articles containing two or more keywords and groups by year.
"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import get_article_keywords
from defoe.papers.query_utils import PreprocessWordType


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of articles containing two or more keywords and
    groups by year.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <YEAR>:
          [
            {
              "words": [<WORD>, <WORD>, ...],
              "count": <COUNT>
            },
            ...
          ],
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
        keywords = [query_utils.normalize(word) for word in list(f)]
    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article)
                       for article in issue.articles])
    # [((year, [word, word, ...]), 1), ...]
    words = articles.map(
        lambda year_article: (
            (year_article[0],
             get_article_keywords(year_article[1],
                                  keywords,
                                  PreprocessWordType.NORMALIZE)),
            1))
    # [((year, [word, word, ...]), 1), ...]
    match_words = words.filter(
        lambda yearword_count: len(yearword_count[0][1]) > 1)
    # [((year, "word, word, ..."), 1), ...]
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
    # [((year, [{"words": [word, word, ...],
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
              word_article_count_list_to_dict(year_wordcount[1])))\
        .collect()
    return result


def word_article_count_list_to_dict(word_counts):
    """
    Converts list of tuples of words and counts of articles these
    occur in into list of dictionaries of lists of words and counts.

    List is of form:

       [("word, word, ...", count), ...]

    Dictionary is of form:

        {
          "words": [<WORD>, <WORD>, ...],
          "count": <COUNT>
        }

    :param word_counts: words and counts
    :type word_counts: list(tuple(list(str or unicode), int))
    :return: dict
    :rtype: dict
    """
    result = []
    for word_count in word_counts:
        result.append({"words": word_count[0].split(","),
                       "count": word_count[1]})
    return result
