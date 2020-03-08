""" 
Pages as a collection of articles to ElasticSearch (ES) using dataframes, and some metadata associated with each document.
"""

from defoe import query_utils
from defoe.nlsArticles.query_utils import clean_headers_page_as_string, get_articles_eb
from pyspark.sql import Row, SparkSession, SQLContext

import yaml, os

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Ingest NLS pages, clean and extract the articles of each to each page, and save them to ES, with some metadata associated with each page.
    Metadata collected: tittle, edition, year, place, archive filename, page filename, page id, num pages, 
    type of archive, model, type_page, header, articles_page, num_articles, num_words  

    Data is saved as Dataframes into ElasticSearch: Index:'nlsArticles'  Type:'Encyclopaedia_Britannica_Articles'

    Example:
    'Encyclopaedia Britannica: or, A dictionary of arts and sciences':
     - archive_name: /home/tdm/datasets/eb_test/144850366
       articles:
       ACQUEST:
        - or Acquist, in law, signifies goods got by purchase or donation. See CoNtiUEST.
       ACQUI:
         - "a town of Italy, in the Dutchy of Montferrat, with a biihop\u2019s see, and\
          \ commodious baths. It was taken by the Spaniards in 1745, and retaken by the\
          \ Piedmontese in 1746; but after this, it was taken again and difrcantled by\
          \ the French, who afterwards forsook it. It is seated on the river Bormio, 25\
          \ miles N.W. of Genoa, and 30 S. of Cafal, 8. 30. E. long. 44. 40. lat."
       ACQUIESCENCE:
         - in commerce, is the consent that a person gives to the determination given either
           by arbitration, orbyaconful

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: "0"
    :rtype: string
    """
    
    text_unit = "page"
    # [(tittle, edition, year, place, archive filename, page filename, 
    #   page id, num pages, type of archive, type of disribution, model)]
    documents = archives.flatMap(
        lambda archive: [(document.title, document.edition, document.year, \
                          document.place, document.archive.filename, document.num_pages, \
                           document.document_type, document.model, document) for document in list(archive)])
    
    # [(tittle, edition, year, place, archive filename, page filename, text_unit, text_unit_id, 
    #   num_text_unit, type of archive, type of disribution, model, clean_page, num_words)]
    pages_clean = documents.flatMap(
        lambda year_document: [(year_document[0], year_document[1], year_document[2],\
                               year_document[3], year_document[4], page.code, text_unit, page.page_id, \
                               year_document[5], year_document[6], year_document[7], \
                               clean_headers_page_as_string(page), len(page.words)) for page in year_document[8]])
    

    # [(tittle, edition, year, place, archive filename, page filename, text_unit, text_unit_id, 
    #   num_text_unit, type of archive, type of disribution, model, type_page, header, articles_page, num_articles, num_words)]
    pages_articles = pages_clean.flatMap(
        lambda clean_page: [(clean_page[0], clean_page[1], clean_page[2],\
                               clean_page[3], clean_page[4], clean_page[5], clean_page[6], clean_page[7], \
                               clean_page[8], clean_page[9], clean_page[10],
                               get_articles_eb(clean_page[11][0],clean_page[11][1],clean_page[11][2]),\
                               clean_page[12])]) 

    pages_header_articles = pages_articles.flatMap(
        lambda articles_page: [(articles_page[0], articles_page[1], articles_page[2],\
                               articles_page[3], articles_page[4], articles_page[5], articles_page[6], articles_page[7], \
                               articles_page[8], articles_page[9], articles_page[10], \
                               articles_page[11][0], articles_page[11][1], articles_page[11][2], articles_page[11][3],\
                               articles_page[12])]) 



    nlsRow=Row("title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "type_page", "header", "articles_page", "num_articles", "num_words")
    sqlContext = SQLContext(context)
    df = sqlContext.createDataFrame(pages_header_articles,nlsRow)
    df = df.drop('_id')
    with open(config_file, "r") as f:
        config = yaml.load(f)
    df.write.format('org.elasticsearch.spark.sql').option('es.nodes', config["host"]).option('es.port', config["port"]).option('es.resource', config["index"],).option('es.nodes.wan.only',"true").mode('overwrite').save()

    return "0"
