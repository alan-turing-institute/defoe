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
    Metadata collected: Tittle, year, place, archive filename, page filename, page id, num pages, type of archive, model, type of preprocess treatment
    
    Example:
    ('Encyclopaedia Britannica; or, A dictionary of arts, sciences, and miscellaneous literature', 
      1810, 'Edinburgh', '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica/191253839', 
      'alto/192209952.34.xml', 'Page5', 446, 'book', 'nls', <PreprocessWordType.NONE:4>, u"Part III. MORAL PHILOSOPHY.....)
    
    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: "0"
    :rtype: string
    """
    # [(year, title, place, publisher, date, document), ...]
    preprocess_type = query_utils.parse_preprocess_word_type("none")
    documents = archives.flatMap(
        lambda archive: [(document.title, document.year, document.place, document.archive.filename, document.num_pages, document.document_type,  document.model, document) for document in list(archive)])
    # [(Tittle, year, place, archive filename, page filename, page id, num pages, type of archive, type of disribution, model, type of preprocess treatment, page_as_string)]
    pages = documents.flatMap(
        lambda year_document: [(year_document[0],year_document[1], year_document[2], year_document[3], page.code, page.page_id, year_document[4], year_document[5], year_document[6], preprocess_type,   
                                    get_page_as_string(page, preprocess_type)) 
                                       for page in year_document[7]])

    pages.saveAsTextFile("hdfs:///user/at003/rosa/text19.txt")
    return "0"
