"""
Counts the total number of documents.
"""


def do_query(archives, data_file=None, logger=None):
    """
    Counts the total number of documents.
    """
    documents = archives.flatMap(lambda archive: list(archive))
    result = documents.count()
    return {"documents": result}
