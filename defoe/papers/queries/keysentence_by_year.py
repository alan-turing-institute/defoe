"""
Counts number of articles in which they are occurences of keysentences
and groups them by year.

Words in articles and keysentences can be normalized, normalized and
stemmed, or normalized and lemmatized (default).
"""

from operator import add
import os.path
import yaml

from defoe import query_utils
from defoe.papers.query_utils import get_article_as_string
from defoe.papers.query_utils import get_sentences_list_matches


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of articles in which they are occurences of
    keysentences and groups them by year.

    Words in articles and keysentences can be normalized, normalized
    and stemmed, or normalized and lemmatized (default).

    config_file must be the path to a configuration file of form:

        preprocess: none|normalize|stem|lemmatize # Optional
        data: <DATA_FILE>

    <DATA_FILE> must be the path to a plain-text data file with a list
    of the keysentences to search for, one per line. If <DATA_FILE> is
    a relative path then it is assumed to be relative to the directory
    in which config_file resides.

    Returns result of form:

        {
            <YEAR>:
            [
                [<SENTENCE>, <NUM_ARTICLES>],
                [<SENTENCE>, <NUM_ARTICLES>],
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
    :return: number of occurrences of keysentences grouped by year
    :rtype: dict
    """
    with open(config_file, "r") as f:
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    keysentences = []
    with open(data_file, 'r') as f:
        for keysentence in list(f):
            k_split = keysentence.split()
            sentence_word = [query_utils.preprocess_word(
                word, preprocess_type) for word in k_split]
            sentence_norm = ''
            for word in sentence_word:
                if sentence_norm == '':
                    sentence_norm = word
                else:
                    sentence_norm += " " + word
            keysentences.append(sentence_norm)
    # [(year, article_string)
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, get_article_as_string(
            article, preprocess_type)) for article in issue.articles])

    # [(year, article_string)
    filter_articles = articles.filter(
        lambda year_article: any(
            keysentence in year_article[1] for keysentence in keysentences))

    # [(year, [keysentence, keysentence]), ...]
    matching_articles = filter_articles.map(
        lambda year_article: (year_article[0],
                              get_sentences_list_matches(
                                  year_article[1],
                                  keysentences)))

    # [[(year, keysentence), 1) ((year, keysentence), 1) ] ...]
    matching_sentences = matching_articles.flatMap(
        lambda year_sentence: [((year_sentence[0], sentence), 1)
                               for sentence in year_sentence[1]])

    # [((year, keysentence), num_keysentences), ...]
    # =>
    # [(year, (keysentence, num_keysentences)), ...]
    # =>
    # [(year, [keysentence, num_keysentences]), ...]
    result = matching_sentences\
        .reduceByKey(add)\
        .map(lambda yearsentence_count:
             (yearsentence_count[0][0],
              (yearsentence_count[0][1], yearsentence_count[1]))) \
        .groupByKey() \
        .map(lambda year_sentencecount:
             (year_sentencecount[0], list(year_sentencecount[1]))) \
        .collect()
    return result
