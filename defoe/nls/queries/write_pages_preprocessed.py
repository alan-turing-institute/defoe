"""
Writes preprocessed pages as string to HDFS textfiles, and some metadata associated with each document.
"""

from defoe import query_utils
from defoe.nls.query_utils import get_page_as_string

import yaml, os

def do_query(archives, config_file=None, logger=None):
    """
    Writes raw pages as string to HDFS textfiles, and some metadata associated with each document.

    Non preprocessed steps are applied to the words extracted from pages.
    Metadata collected: Tittle, year, place, archive filename, page filename, page id, num pages, type of archive, type of preprocess treatment
 
    config_file must be the path to a configuration file with the preoprocessed type to apply to the pages' words

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
    documents = archives.flatMap(
        lambda archive: [(document.title, document.year, document.place, document.archive.filename, document.num_pages, document.document_type,  document) for document in list(archive)])
    # [(year, title, place, publisher, date, page_string)
    pages = documents.flatMap(
        lambda year_document: [(year_document[0],year_document[1], year_document[2], year_document[3], page.code, page.page_id, year_document[4], year_document[5], perprocess_type,   
                                    get_page_as_string(page, preprocess_type)) 
                                       for page in year_document[6]])

    pages.saveAsTextFile("hdfs:///user/at003/rosa/text16.txt")
    return "0"
