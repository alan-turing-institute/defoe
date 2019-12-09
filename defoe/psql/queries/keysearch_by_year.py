"""
Read from PostgreSQL table, and counts number of occurrences of keywords or keysentences and groups by year.
"""

from operator import add
from defoe import query_utils
from defoe.psql.query_utils import get_sentences_list_matches, blank_as_null
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when


import yaml, os

def do_query(df, config_file=None, logger=None, context=None):
    """
    Read from HDFS, and counts number of occurrences of keywords or keysentences and groups by year.
    We have an entry in the HFDS file with the following information: 

    nlsRow=Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem", "num_words")


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
    preprocess_config = config["preprocess"]
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    
    # Filter out the pages that are null, which model is nls, and select only 2 columns: year and the page as string (either raw or preprocessed).
    if preprocess_config == "normalize":
        fdf = df.withColumn("source_text_norm", blank_as_null("source_text_norm"))
        newdf=fdf.filter(fdf.source_text_norm.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.source_text_norm)
    elif preprocess_config == "lemmatize":
        fdf = df.withColumn("source_text_lemmatize", blank_as_null("source_text_lemmatize"))
        newdf=fdf.filter(fdf.source_text_lemmatize.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.source_text_lemmatize)
    elif preprocess_config == "stem":
        fdf = df.withColumn("source_text_stem", blank_as_null("source_text_stem"))
        newdf=fdf.filter(fdf.source_text_stem.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.source_text_stem)
    else: 
        fdf = df.withColumn("source_text_clean", blank_as_null("source_text_clean"))
        newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.source_text_clean)
   
    pages=newdf.rdd.map(tuple)
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
    

    filter_pages = pages.filter(
        lambda year_page: any( keysentence in year_page[1] for keysentence in keysentences))
    
    # [(year, [keysentence, keysentence]), ...]
    # We also need to convert the string as an integer spliting first the '.
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
