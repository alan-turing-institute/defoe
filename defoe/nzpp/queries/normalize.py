"""
Counts total number of articles and words per year.

This can be useful if wanting to see how the average number of
articles and words change over time, for example.
"""


def do_query(all_articles, config_file=None, logger=None):
    """
    Counts total number of articles and words per year.

    Returns result of form:

        {
          <YEAR>: [<NUM_ALL_ARTICLES>, <NUM_ARTICLES>, <NUM_WORDS>],
          ...
        }

    :param all_articles RDD of defoe.nzpp.articles.Articles
    :type all_articles: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of articles and words per year
    :rtype: list
    """
    # [(article, ...)]
    articles = all_articles.flatMap(
        lambda articles: [article for article in articles.articles])
    # [(year, 1, num_words)]
    counts = articles.map(
        lambda article: (article.date.year, (1, len(article.words))))
    result = counts \
        .reduceByKey(lambda x, y:
                     tuple(i + j for i, j in zip(x, y))) \
        .map(lambda year_data: (year_data[0], list(year_data[1]))) \
        .collect()
    return result
