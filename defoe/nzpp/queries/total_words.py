"""
Counts total number of words.
"""

from operator import add


def do_query(all_articles, config_file=None, logger=None):
    """
    Iterate through articles and count total number of articles
    and total number of words.

    Returns result of form:

        {
          "num_articles": num_articles,
          "num_words": num_words
        }

    :param all_articles: RDD of defoe.nzpp.articles.Articles
    :type all_articles: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of articles and words
    :rtype: dict
    """
    # [article, article, ...]
    articles = all_articles.flatMap(lambda articles:
                                    [article for article in articles.articles])
    # [num_words, num_words, ...]
    num_words = articles.map(lambda article: len(list(article.words)))
    result = [articles.count(), num_words.reduce(add)]
    return {"num_articles": result[0],
            "num_words": result[1]}
