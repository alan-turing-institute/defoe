"""
Counts total number of pages.
"""

from operator import add


def do_query(archives, config_file=None, logger=None):
    """
    Iterate through archives and count total number of documents
    and total number of pages.

    Returns result of form:

        {
          "num_documents": num_documents,
          "num_pages": num_pages
        }

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents and pages
    :rtype: dict
    """
    # [archive, archive, ...]
    documents = archives.flatMap(lambda archive: list(archive))
    # [num_pages, num_pages, ...]
    num_pages = documents.map(lambda document: document.num_pages)
    result = [documents.count(), num_pages.reduce(add)]
    return {"num_documents": result[0],
            "num_pages": result[1]}
