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

    :param issues: RDD of defoe.xml.document.Document
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: unique root elements and frequencies
    :rtype: dict
    """
    # [(element, 1), (element, 1), ...]
    elements = documents.map(lambda document:
                             (document.root_element, 1))

    # [(element, 1), (element, 1), ...]
    # =>
    # [(element, count), (element, count), ...]
    element_counts = elements. \
        reduceByKey(add). \
        collect()
    return element_counts
