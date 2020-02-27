"""
Gets concordance of window for keysentence and groups by date.
"""

from operator import add
from defoe import query_utils
from defoe.nls.query_utils import get_pages_matches_no_prep
from defoe.hdfs.query_utils import blank_as_null
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when


import yaml, os

def do_query(df, config_file=None, logger=None, context=None):
    """
    Gets concordance using a window of words, for keywords and groups by date.

    Data in ES have the following colums:

    "title",  "edition", "year", "place", "archive_filename", 
    "source_text_filename", "text_unit", "text_unit_id", 
    "num_text_unit", "type_archive", "model", "source_text_raw", 
    "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem",
    "num_words"

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:
          [(year, [(title, edition, archive_filename, filename, word,corcondance),
              (title, edition, archive_filename, filename, word, concordance ), ...]), ...]


    :param issues: RDD of defoe.alto.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by date
    :rtype: dict
    """

    with open(config_file, "r") as f:
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    preprocess_config = config["preprocess"]
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    
    # Filter out the pages that are null, which model is nls, and select only 2 columns: year and the page as string (either raw or preprocessed).
    if preprocess_config == "normalize":
        fdf = df.withColumn("source_text_norm", blank_as_null("source_text_norm"))
        newdf=fdf.filter(fdf.source_text_norm.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.source_text_norm)
    elif preprocess_config == "lemmatize":
        fdf = df.withColumn("source_text_lemmatize", blank_as_null("source_text_lemmatize"))
        newdf=fdf.filter(fdf.source_text_lemmatize.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.source_text_lemmatize)
    elif preprocess_config == "stem":
        fdf = df.withColumn("source_text_stem", blank_as_null("source_text_stem"))
        newdf=fdf.filter(fdf.source_text_stem.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.source_text_stem)
    else: 
        fdf = df.withColumn("source_text_clean", blank_as_null("source_text_clean"))
        newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.source_text_clean)


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
        lambda year_page: any( keysentence in year_page[5] for keysentence in keysentences))


    # [(year, title, edition, archive_filename, filename, text, [(word, idx), (word, idx) ...]), ...]
    maching_idx = filter_pages.map(
        lambda year_page: (
            (year_page[0],
             year_page[1],
             year_page[2],
             year_page[3],
             year_page[4],
             year_page[5],
             get_text_keyword_idx(year_page[5],
                                     keysentences))
        )
    )

    # [(year, [(title, edition, archive_filename, filename, word, [concordance, ...]), ...])]
    concordance_words = matching_idx.flatMap(
        lambda year_idx: [
            (year_idx[0],
             (year_idx[1],
              year_idx[2],
              year_idx[3],
              year_idx[4],
              word_idx[0],
              get_concordance(year_idx[5],
                              word_idx[0],
                              word_idx[1],
                              window))
            for word_idx in year_idx[6]])



    # [(year, [(title, edition, archive_filename, filename, word,corcondance),
    #          (title, edition, archive_filename, filename, word, concordance ), ...]), ...]
    result = concordance_words.groupByKey() \
        .map(lambda year_match:
             (year_match[0], list(year_match[1]))) \
        .collect()
    return result
