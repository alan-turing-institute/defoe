"""
Writes raw pages as string to HDFS textfiles, and some metadata associated with each document.
"""

from defoe import query_utils
from defoe.nls.query_utils import get_page_as_string

import yaml, os

def do_query(archives, config_file=None, logger=None):
    """
    Writes raw pages as string to HDFS textfiles, and some metadata associated with each document.

    Non preprocessed steps are applied to the words extracted from pages.
    Metadata associated: Year (e.g. 1810), title (e.g. Encyclopaedia Britannica; or, A dictionary of arts, sciences, and miscellaneous literature),
                         place (e.g. stk), publisher (none), date of the document (1810). 
    And page as string:  'Part III. MORAL PHILOSOPHY. 22,6 Unfat isfied defires of exiftence and happi- \xbbeis. Motives to ^ood minds, and feme traces of which arc found in the Virtue.'
 
    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped by year
    :rtype: dict
    """
    # [(year, title, place, publisher, date, document), ...]
    preprocess_type = query_utils.parse_preprocess_word_type("none")
    documents = archives.flatMap(
        lambda archive: [(document.year, document.title, document.place, document.publisher, document.date, document) for document in list(archive)])
    # [(year, title, place, publisher, date, page_string)
    pages = documents.flatMap(
        lambda year_document: [(year_document[0],year_document[1], year_document[2], year_document[3], year_document[4], 
                                    get_page_as_string(page, preprocess_type)) 
                                       for page in year_document[5]])

    #pages.saveAsTextFile("hdfs:///user/at003/rosa/text7.txt")
    return "0"
