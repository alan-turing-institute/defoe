""" 
Pages as string to HDFS CSv files (using dataframes), and some metadata associated with each document.
"""

from defoe import query_utils
from defoe.nls.query_utils import get_page_as_string
from pyspark.sql import Row, SparkSession, SQLContext
from pyspark.sql import DataFrameWriter

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, applies all 4 preprocess treatments (none, normalize, lemmatize, stem) to each page, and save them to HDFS CSV files, with some metadata associated with each page.
    Metadata collected: tittle, edition, year, place, archive filename, page filename, page id, num pages, 
    type of archive, model, page_string_raw, page_string_norm, page_string_lemmatize, page_string_stem, num_page_words

    Data is saved as Dataframes into HDFS CSV files 


    Example:
    ('Encyclopaedia Britannica; or, A dictionary of arts, sciences, and miscellaneous literature', 'Fourth edition ...', 
      1810, 'Edinburgh', '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica/191253839', 
      'alto/192209952.34.xml', 'Page5', 446, 'book', 'nls',  u"Part III. MORAL PHILOSOPHY....., u"part iii moral ...", u"part iii moral ...", u"part iii moral...",'46')
    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: "0"
    :rtype: string
    """
    
    preprocess_none = query_utils.parse_preprocess_word_type("none")
    preprocess_normalize = query_utils.parse_preprocess_word_type("normalize")
    preprocess_lemmatize = query_utils.parse_preprocess_word_type("lemmatize")
    preprocess_stem = query_utils.parse_preprocess_word_type("stem")
    documents = archives.flatMap(
        lambda archive: [(document.title, document.edition, document.year, \
                          document.place, document.archive.filename, document.num_pages, \
                           document.document_type, document.model, document) for document in list(archive)])
    # [(tittle, edition, year, place, archive filename, page filename, 
    #   page id, num pages, type of archive, type of disribution, model, page_string_raw, page_string_norm, 
    #   page_string_lemmatize, page_string_stem, num_page_words )]
    pages = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                               year_document[3], year_document[4], page.code, page.page_id, \
                               year_document[5], year_document[6], year_document[7], get_page_as_string(page, preprocess_none), \
                               get_page_as_string(page, preprocess_normalize), \
                               get_page_as_string(page, preprocess_lemmatize), get_page_as_string(page, preprocess_stem),\
                                len(page.words)) for page in year_document[8]])


    nlsRow=Row("title","edition","year", "place", "archive_filename", "page_filename","page_id","num_pages","type_archive", \
                "model","page_string_raw", "page_string_norm", "page_string_lemmatize", "page_string_stem", "num_page_words")
    sqlContext = SQLContext(context)
    df = sqlContext.createDataFrame(pages,nlsRow)
   
    with open(config_file, "r") as f:
        config = yaml.load(f)
    url = "jdbc:postgresql://%s:%s/%s" % (config["host"],config["port"],config["database"])
    properties = {"user": config["user"] ,"driver": config["driver"]}
    
    mode = "overwrite"
    df.write.jdbc(url=url, table=config["table"], mode=mode, properties=properties)
    return "0"
