"""
Given a filename create a dataframe
"""

from pyspark.sql import SQLContext

def filename_to_object(filename, context):
    """
    Given a filename create a defoe.books.archive.Archive.  If an error
    arises during its creation this is caught and returned as a
    string.

    :param filename: filename
    :type filename: str or unicode
    :return: tuple of form (Archive, None) or (filename, error message),
    if there was an error creating Archive
    :rtype: tuple(defoe.books.archive.Archive | str or unicode, str or unicode)
    """

    lines=open(filename).readlines()
    fields=lines[1].split(",")
    #index,type_name
    es_index=fields[0]
    es_type_name=fields[1]
    sqlContext = SQLContext(context)
    reader = sqlContext.read.format("org.elasticsearch.spark.sql").option("es.read.metadata", "true").option("es.nodes.wan.only","true").option("es.port","9200").option("es.net.ssl","false").option("es.nodes", "http://localhost")
    df = reader.load(es_index+"/"+es_type_name)
    return df
