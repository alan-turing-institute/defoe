"""
Counts total number of documents.
"""


def do_query(archives, data_file=None, logger=None):
    """
    Iterate through archives and count total number of documents.
    Returns result of form:

        {"num_documents": num_documents}

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param data_file: query configuration file (unused)
    :type data_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents
    :rtype: dict
    """
    # [Archive, Archive, ...]
    documents = archives.flatMap(lambda archive: list(archive))
    num_documents = documents.count()
    return {"num_documents": num_documents}
