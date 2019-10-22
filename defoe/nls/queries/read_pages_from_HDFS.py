"""
Read from HDFS file, and counts number of occurrences of keywords or keysentences and groups by year.
"""

from operator import add
from defoe import query_utils
from defoe.nls.query_utils import get_page_as_string
from defoe.nls.query_utils import get_sentences_list_matches

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Read from HDFS, and counts number of occurrences of keywords or keysentences and groups by year.
    We have an entry in the HFDS file with the following information: 
	- tittle, edition, year, place, archive filename, page filename, page id, num pages, type of archive, model, type of preprocess treatment, prep_page_string

    Notice, that year is in position "2", and the preprocessed page as an string is in position 11. However, the information per entry has been saved as an string.
    So, we need first to split the string into elements. And later get the year (position 2) and page (position 11). 


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
    
    pages_hdfs = context.textFile("hdfs:///user/at003/rosa/demo_text1.txt") 
   
    pages = pages_hdfs.map(
       lambda p_string: p_string.strip('][').split("\',")) 

    filter_pages = pages.filter(
        lambda year_page: any(
            keysentence in year_page[11][:-1] for keysentence in keysentences))
    
    
    # [(year, [keysentence, keysentence]), ...]
    matching_pages = filter_pages.map(
        lambda year_page: (int(year_page[2].split("\'")[1]),
                              get_sentences_list_matches(
                                  year_page[11][:-1],
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
