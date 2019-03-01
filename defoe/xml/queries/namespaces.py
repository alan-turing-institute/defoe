"""
Finds every unique namespace (NAMESPACE) and its frequency.
"""

from operator import add


def do_query(documents, config_file=None, logger=None):
    """
    Finds every unique namespace (NAMESPACE) and its frequency.

    Returns result of form:

        {
          <NAMESPACE>: <COUNT>,
          ...
        }

    :param issues: RDD of defoe.xml.document.Document
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: unique namespaces and frequencies
    :rtype: dict
    """
    # [(namespace, 1), (namespace, 1), ...]
    namespaces = documents.map(lambda document:
                               (document.namespaces, 1))

    # [(namespace, 1), (namespace, 1), ...]
    # =>
    # [(namespace, count), (namespace, count), ...]
    namespace_counts = namespaces. \
        reduceByKey(add). \
        collect()
    return namespace_counts
