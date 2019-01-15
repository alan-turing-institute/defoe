"""
Counts the total number of words across all documents.
"""

from operator import add


def do_query(archives, data_file=None, logger=None):
    """
    Counts the total number of words across all documents.
    """
    documents = archives.flatMap(lambda archive: list(archive))
    word_counts = documents.map(lambda document: len(list(document.words())))
    result = [documents.count(), word_counts.reduce(add)]
    return {"documents": result[0], "words": result[1]}
