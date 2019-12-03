"""
Counts number of occurrences of keywords or keysentences and groups by year.
"""

from operator import add

from defoe import query_utils
from defoe.nls.query_utils import preprocess_clean_page, clean_page_as_string
from defoe.nls.query_utils import get_sentences_list_matches

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Counts number of occurrences of keywords or keysentences and groups by year.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords/keysentences and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <YEAR>:
          [
            [<SENTENCE|WORD>, <NUM_SENTENCES|WORDS>],
            ...
          ],
          <YEAR>:
          ...
        }

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
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
    # [(year, document), ...]
    documents = archives.flatMap(
        lambda archive: [(document.year, document) for document in list(archive)])
    # [(year, page_string)
    
    clean_pages = documents.flatMap(
        lambda year_document: [(year_document[0], 
                                    clean_page_as_string(page)) 
                                       for page in year_document[1]])
    pages = clean_pages.flatMap(
        lambda cl_page: [(cl_page[0], 
                                    preprocess_clean_page(cl_page[1], preprocess_type))]) 
    # [(year, page_string)
    # [(year, page_string)
    filter_pages = pages.filter(
        lambda year_page: any(
            keysentence in year_page[1] for keysentence in keysentences))
    
    # [(year, [keysentence, keysentence]), ...]
    matching_pages = filter_pages.map(
        lambda year_page: (year_page[0],
                              get_sentences_list_matches(
                                  year_page[1],
                                  keysentences)))

    # [[(year, keysentence), 1) ((year, keysentence), 1) ] ...]
    matching_sentences = matching_pages.flatMap(
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
