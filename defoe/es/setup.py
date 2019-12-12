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
    #index,host,port
    es_index=fields[0]
    es_host=fields[1]
    es_port=fields[2].rstrip('\n')

    sqlContext = SQLContext(context)
    reader = sqlContext.read.format("org.elasticsearch.spark.sql").option("es.read.metadata", "true").option("es.nodes.wan.only","true").option("es.port",es_port).option("es.net.ssl","false").option("es.nodes", "http://"+es_host)
    df = reader.load(es_index)
    return df

