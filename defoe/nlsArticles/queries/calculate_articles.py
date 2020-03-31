""" 
"""

from defoe import query_utils
from defoe.nlsArticles.query_utils import clean_headers_page_as_string, get_articles_eb
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, applies all 4 preprocess treatments (none, normalize, lemmatize, stem) to each page, and save them to ES, with some metadata associated with each page.
    Metadata collected: tittle, edition, year, place, archive filename, page filename, page id, num pages, 
    type of archive, model, source_text_raw, source_text_norm, source_text_lemmatize, source_text_stem, source_text_spacy_nlp, num_page_words

    Data is saved as Dataframes into ElasticSearch: Index:'nls'  Type:'Encyclopaedia_Britannica'

    Example:
    ('Encyclopaedia Britannica,"Seventh edition, Volume 13, LAB-Magnetism",1842,Edinburgh,/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica/193108323,alto/193201394.34.xml,page,Page9,810,book,nls,"THE ENCYCLOPAEDIA BRITANNICA DICTIONARY OF ARTS, SCIENCES, AND GENERAL LITERATURE. SEVENTH EDITION, i WITH PRELIMINARY DISSERTATIONS ON THE HISTORY OF THE SCIENCES, AND OTHER EXTENSIVE IMPROVEMENTS AND ADDITIONS; INCLUDING THE LATE SUPPLEMENT. A GENERAL INDEX, AND NUMEROUS ENGRAVINGS. VOLUME XIII. ADAM AND CHARLES BLACK, EDINBURGH; M.DCCC.XLII.","THE ENCYCLOPAEDIA BRITANNICA DICTIONARY OF ARTS, SCIENCES, AND GENERAL LITERATURE. SEVENTH EDITION, i WITH PRELIMINARY DISSERTATIONS ON THE HISTORY OF THE SCIENCES, AND OTHER EXTENSIVE IMPROVEMENTS AND ADDITIONS; INCLUDING THE LATE SUPPLEMENT. A GENERAL INDEX, AND NUMEROUS ENGRAVINGS. VOLUME XIII. ADAM AND CHARLES BLACK, EDINBURGH; M.DCCC.XLII.",the encyclopaedia britannica dictionary of arts sciences and general literature seventh edition i with preliminary dissertations on the history of the sciences and other extensive improvements and additions including the late supplement a general index and numerous engravings volume xiii adam and charles black edinburgh mdcccxlii,the encyclopaedia britannica dictionary of art science and general literature seventh edition i with preliminary dissertation on the history of the science and other extensive improvement and addition including the late supplement a general index and numerous engraving volume xiii adam and charles black edinburgh mdcccxlii,the encyclopaedia britannica dictionari of art scienc and gener literatur seventh edit i with preliminari dissert on the histori of the scienc and other extens improv and addit includ the late supplement a gener index and numer engrav volum xiii adam and charl black edinburgh mdcccxlii,46')

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: "0"
    :rtype: string
    """
    
    # [(tittle, edition, year, archive filename)]
    documents = archives.flatMap(
        lambda archive: [(document.title, document.edition, document.year, \
                          document.archive.filename, document) for document in list(archive)])

    # [(tittle, edition, year, place, archive filename, page filename, text_unit_id,clean_page)]
    pages_clean = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                                year_document[3], page.code, page.page_id, \
                                clean_headers_page_as_string(page)) for page in year_document[4]])

    articles_clean = pages_clean.map(
              lambda page_document: (page_document[0], page_document[1], page_document[2], page_document[3], page_document[4], page_document[5], get_articles_eb(page_document[6][0],page_document[6][1],page_document[6][2])))


    r_articles_pages = articles_clean.map(
              lambda articles_page:
              (articles_page[0], 
               { "edition": articles_page[1], 
                  "year":   articles_page[2],
                  "archive_name": articles_page[3],
                  "page_filename": articles_page[4],
                  "text_unit id": articles_page[5], 
                  "type": articles_page[6][0],
                  "header": articles_page[6][1],
                  "num_articles": articles_page[6][3]}))
    
    #"articles": articles_page[6][2], 
    result = r_articles_pages \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result

