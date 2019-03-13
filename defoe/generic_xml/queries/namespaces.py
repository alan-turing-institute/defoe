"""
Finds every unique namespace and its frequency.
"""

from operator import add


def do_query(documents, config_file=None, logger=None):
    """
    Finds every unique namespace and its frequency.

    Returns result of form:

        {
          <NAMESPACE>: <COUNT>,
          ...
        }

    :param documents: RDD of defoe.generic_xml.document.Document
    :type documents: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: unique namespaces and frequencies
    :rtype: dict
    """
    namespaces = documents.flatMap(lambda document:
                                   get_namespaces(document))
    namespace_counts = namespaces. \
        reduceByKey(add). \
        collect()
    return namespace_counts


def get_namespaces(document):
    """
    Extract namespaces from a document.

    :param document: defoe.generic_xml.document.Document
    :type document: defoe.generic_xml.document.Document
    :return: list of (URL, 1) for each namespace URL in the
    document
    :rtype: list(tuple(str or unicode, 1))
    """
    return [(tag_url[1], 1) for tag_url in list(document.namespaces.items())]
