"""
Counts total size of document files in bytes.
"""

from operator import add


def do_query(documents, config_file=None, logger=None):
    """
    Iterate through documents and count total size of document files
    in bytes.
    Returns result of form:

        {"total_size": total_size}

    :param documents: RDD of defoe.document.Document
    :type documents: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total size of document files in bytes
    :rtype: dict
    """
    file_sizes = documents.map(lambda document: document.filesize)
    return {"total_size": file_sizes.reduce(add)}
