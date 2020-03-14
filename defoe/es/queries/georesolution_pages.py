""" 
Identify the locations per page and geo-resolve them.
"""

from defoe import query_utils
from defoe.nls.query_utils import georesolve_page_2
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, applies scpaCy NLP pipeline for identifying the possible locations of each page. And applies the edinburgh geoparser for getting the latituted and longitude of each of them.
    Before applying the geoparser, two clean steps are applied - long-S and hyphen words. 
    
    Example:


    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: "0"
    :rtype: string
    """
   
    lang_model = "en_core_web_lg"
    fdf = df.withColumn("source_text_clean", blank_as_null("source_text_clean"))
   
    newdf=fdf.filter(fdf.source_text_clean.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.title, fdf.edition, fdf.archive_filename, fdf.source_text_filename, fdf.text_unit_id, fdf.source_text_clean)

    pages=newdf.rdd.map(tuple)
    matching_pages = geo_xml_pages.map(
        lambda geo_page:
        (geo_page[0],
         {"title": geo_page[1],
          "edition": geo_page[2],
          "archive": geo_page[3], 
          "page_filename": geo_page[4],
          "text_unit id": geo_page[5],
          "lang_model": "geoparser_original", 
          "georesolution_page": georesolve_page_2(geo_page[5],lang_model)}))
    
    result = matching_pages \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result
