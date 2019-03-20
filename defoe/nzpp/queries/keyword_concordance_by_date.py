"""
Gets concordance for keywords and groups by date.
"""

from defoe import query_utils
from defoe.papers.query_utils import get_article_keywords


def do_query(all_articles, config_file=None, logger=None):
    """
    Gets concordance for keywords and groups by date.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <DATE>:
          [
            {
              "title": <TITLE>,
              "paper_name": <NAME>,
              "content": <PAGE_CONTENT>,
              "word": <WORD>,
              "filename": <FILENAME>
            },
            ...
          ],
          <DATE>:
          ...
        }

    :param all_articles: RDD of defoe.npzz.articles.Articles
    :type all_articles: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by date
    :rtype: dict
    """
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.normalize(word) for word in list(f)]

    # [(article, ...)]
    articles = all_articles.flatMap(
        lambda articles: [article for article in articles.articles])

    # [(article, words), ...]
    # This exploits defoe.papers.query_utils.get_article_keywords
    # use of only a "words" property from the given article.
    articles_words = articles.map(
        lambda article: (article,
                         get_article_keywords(article, keywords)))

    # [(article, words), ...]
    filtered_words = articles_words.filter(
        lambda article_words: len(article_words[1]) > 0)

    # [(article, word), ...]
    article_words = filtered_words.flatMap(
        lambda article_words: [(article_words[0], word)
                               for word in article_words[1]])

    # [(article, word), ...]
    # =>
    # [(date, {"title": title, ...}), ...]
    matching_docs = article_words.map(
        lambda article_word:
        (article_word[0].date.date(),
         {"title": article_word[0].title_string,
          "paper_name": article_word[0].paper_name,
          "content": article_word[0].words_string,
          "word":  article_word[1],
          "filename": article_word[0].filename}))

    # [(date, {"title": title, ...}), ...]
    # =>
    # [(date, [{"title": title, ...], {...}), ...)]
    result = matching_docs \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result
