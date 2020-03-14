"""
Geoparser a NLS document - original geoparsing 
"""

from operator import add
from defoe import query_utils
from defoe.hdfs.query_utils import get_sentences_list_matches, blank_as_null
from defoe.nls.query_utils import georesolve_page
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, when


import yaml, os

def do_query(df, config_file=None, logger=None, context=None):
    """
    Read from HDFS, and counts number of occurrences of keywords or keysentences and groups by year.
    We have an entry in the HFDS file with the following information: 
    
    "title",  "edition", "year", "place", "archive_filename",  "source_text_filename", 
    "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", 
    "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem", "num_words"

    config_filep 

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
    
    
    fdf = df.withColumn("source_text_clean", blank_as_null("source_text_clean"))
   
    newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.text_unit_id, fdf.source_text_clean)

    pages=newdf.rdd.map(tuple)
    
    geo_xml_pages = pages.flatMap(
        lambda clean_page: [(clean_page[0], clean_page[1], clean_page[2],\
                               clean_page[3], clean_page[4], clean_page[5], query_utils.geoparser_cmd(clean_page[6]))])
    
     
    matching_pages = geo_xml_pages.map(
        lambda geo_page:
        (geo_page[0],
         {"title": geo_page[1],
          "edition": geo_page[2],
          "archive": geo_page[3], 
          "page_filename": geo_page[4],
          "text_unit id": geo_page[5],
          "lang_model": "geoparser_original", 
          "georesolution_page": query_utils.geoparser_coord_xml(geo_page[6])}))

    
    result = matching_pages \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result
