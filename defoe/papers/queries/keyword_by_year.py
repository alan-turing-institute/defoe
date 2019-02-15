"""
Counts number of occurrences of keywords and groups by year.
"""

from operator import add

from defoe import query_utils


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of occurrences of keywords and groups by year.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <YEAR>:
          [
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
        keywords = [query_utils.normalize(word) for word in list(f)]
    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article) for article in issue.articles])
    # [((year, word), 1), ...]
    words = articles.flatMap(
        lambda year_article: [
            ((year_article[0], query_utils.normalize(word)), 1)
            for word in year_article[1].words
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
