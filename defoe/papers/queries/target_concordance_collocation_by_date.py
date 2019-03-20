"""
Gets concordance and collocation for keywords occurring in articles
which have a target word and groups the results by date.

Words in articles, target words and keywords can be normalized,
normalized and stemmed, or normalized and lemmatized (default).
"""

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.papers.query_utils import get_article_idx
from defoe.papers.query_utils import get_concordance
from defoe.query_utils import PreprocessWordType


PREPROCESS_TYPE = PreprocessWordType.LEMMATIZE
""" Default word pre-processing type """


WINDOW_SIZE = 10
""" Default window size for concordance """


def do_query(issues, config_file=None, logger=None):
    """
    Gets concordance and collocation for keywords occurring in
    articles which have a target word and groups the results by date.

    Words in articles, target words and keywords can be normalized,
    normalized and stemmed, or normalized and lemmatized (default).

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line. The first word
    is assumed to be the target word.

    Returns result of form:
        <YEAR>:
        - [<FILENAME>, <WORD>, <CONCORDANCE>, <OCR>]
        - [<FILENAME>, <WORD>, <CONCORDANCE>, <OCR>]

    :param issues: RDD of defoe.alto.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by year
    :rtype: dict
    """
    window = WINDOW_SIZE
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.preprocess_word(
            word, PREPROCESS_TYPE) for word in list(f)]
    target_word = keywords[0]
    # [(year, article, filename, ocr), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article, issue.filename, article.quality)
                       for article in issue.articles])
    # [(year, article,filename, ocr), ...]
    target_articles = articles.filter(
        lambda year_article: article_contains_word(
            year_article[1], target_word, PREPROCESS_TYPE))

    # [(year, (article, filename, [(word, idx), (word, idx) ...], ocr), ...]
    matching_idx = target_articles.map(
        lambda year_article: (
            (year_article[0],
             get_article_idx(year_article[1],year_article[2], keywords, PREPROCESS_TYPE, year_article[3]))
            ))

   # [(year, (filename, word, corcondance, ocr), (filename, word, concordance, ocr) ...), ...]
    concordance_words = matching_idx.flatMap(
        lambda target_article: [
            (target_article[0], get_concordance(target_article[1][0],target_article[1][1], match, window, PREPROCESS_TYPE, target_article[1][3]))
            for match in target_article[1][2]])
    
    
    # [(year,(filename, [word, concodance], ocr), (filename,[word, concordance], ocr), ...]
    result = concordance_words.groupByKey() \
        .map(lambda year_wordcount:
             (year_wordcount[0], list(year_wordcount[1]))) \
        .collect()
    return result
