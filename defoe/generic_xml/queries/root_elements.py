"""
Finds every unique root element and its frequency.
"""

from operator import add


def do_query(documents, config_file=None, logger=None):
    """
    Finds every unique root element and its frequency.

    Returns result of form:

        {
          <ELEMENT>: <COUNT>,
          ...
        }

    :param documents: RDD of defoe.generic_xml.document.Document
    :type documents: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: unique root elements and frequencies
    :rtype: dict
    """
    elements = documents.map(lambda document:
                             (document.root_element_tag, 1))
    element_counts = elements. \
        reduceByKey(add). \
        collect()
    return element_counts
