"""
Gets concordance and collocation for keywords occurring in articles
which have a target word and groups the results by date.

Words in articles, target words and keywords can be normalized,
normalized and stemmed, or normalized and lemmatized (default).
"""

import os.path
import yaml

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.papers.query_utils import get_article_keyword_idx
from defoe.papers.query_utils import get_concordance


def do_query(issues, config_file=None, logger=None):
    """
    Gets concordance and collocation for keywords occurring in
    articles which have a target word and groups the results by date.
    Words in articles, target words and keywords can be normalized,
    normalized and stemmed, or normalized and lemmatized (default).
    A window size (default 10) determines the size of the concordance
    returned.
    config_file must be the path to a configuration file of form:

        preprocess: none|normalize|stem|lemmatize # Optional
        window: <WINDOW_SIZE> # Optional
        data: <DATA_FILE>

    <DATA_FILE> must be the path to a plain-text data file with a list
    of keywords to search for, one per line. The first word is assumed
    to be the target word. If <DATA_FILE> is a relative path then it
    is assumed to be relative to the directory in which config_file
    resides.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line. The first word
    is assumed to be the target word.
    Returns result of form:

        {
            <YEAR>:
            [
                [<FILENAME>, <WORD>, <CONCORDANCE>, <OCR>],
                [<FILENAME>, <WORD>, <CONCORDANCE>, <OCR>],
                ...
            ],
            <YEAR>:
            ...
        }

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
    with open(config_file, "r") as f:
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    window = query_utils.extract_window_size(config)
    keywords = []
    with open(data_file, "r") as f:
        keywords = [query_utils.preprocess_word(
            word, preprocess_type) for word in list(f)]
    target_word = keywords[0]

    # [(year, article, filename, ocr), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year,
                        article,
                        issue.filename,
                        article.quality)
                       for article in issue.articles])
    # [(year, article, filename, ocr), ...]
    target_articles = articles.filter(
        lambda year_article_file_ocr: article_contains_word(
            year_article_file_ocr[1], target_word, preprocess_type))
    # [(year, article, filename, [(word, idx), (word, idx) ...], ocr), ...]
    matching_idx = target_articles.map(
        lambda year_article_file_ocr: (
            (year_article_file_ocr[0],
             year_article_file_ocr[1],
             year_article_file_ocr[2],
             get_article_keyword_idx(year_article_file_ocr[1],
                                     keywords,
                                     preprocess_type),
             year_article_file_ocr[3])
        )
    )
    # [(year, [(filename, word, [concordance, ...], ocr), ...])]
    concordance_words = matching_idx.flatMap(
        lambda year_article_file_matches_ocr: [
            (year_article_file_matches_ocr[0],
             (year_article_file_matches_ocr[2],
              word_idx[0],
              get_concordance(year_article_file_matches_ocr[1],
                              word_idx[0],
                              word_idx[1],
                              window,
                              preprocess_type),
              year_article_file_matches_ocr[4]))
            for word_idx in year_article_file_matches_ocr[3]])

    # [(year, [(filename, word, corcondance, ocr),
    #          (filename, word, concordance, ocr), ...]), ...]
    result = concordance_words.groupByKey() \
        .map(lambda year_match:
             (year_match[0], list(year_match[1]))) \
        .collect()
    return result
