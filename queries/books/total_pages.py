"""
Counts the total number of pages across all books.
"""

from operator import add


def do_query(archives, data_file=None, logger=None):
    """
    Counts the total number of pages across all books.
    """
    books = archives.flatMap(lambda archive: list(archive))
    page_counts = books.map(lambda book: book.pages)
    result = [books.count(), page_counts.reduce(add)]
    return {"books": result[0], "pages": result[1]}
