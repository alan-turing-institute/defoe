"""
Counts total number of words.
"""

from operator import add


def do_query(archives, config_file=None, logger=None):
    """
    Iterate through archives and count total number of documents
    and total number of words.

    Returns result of form:

        {
          "num_documents": num_documents,
          "num_words": num_words
        }

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents and words
    :rtype: dict
    """
    # [archive, archive, ...]
    documents = archives.flatMap(lambda archive: list(archive))
    # [num_words, num_words, ...]
    num_words = documents.map(lambda document: len(list(document.words())))
    result = [documents.count(), num_words.reduce(add)]
    return {"num_documents": result[0],
            "num_words": result[1]}
