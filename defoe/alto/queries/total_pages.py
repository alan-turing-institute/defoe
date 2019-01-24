"""
Counts the total number of pages across all documents.
"""

from operator import add


def do_query(archives, data_file=None, logger=None):
    """
    Counts the total number of pages across all documents.
    """
    documents = archives.flatMap(lambda archive: list(archive))
    page_counts = documents.map(lambda document: document.num_pages)
    result = [documents.count(), page_counts.reduce(add)]
    return {"documents": result[0], "pages": result[1]}
