"""
Counts the total number of words across all books.
"""

from operator import add


def do_query(archives, data_file=None, logger=None):
    """
    Counts the total number of words across all books.
    """
    books = archives.flatMap(lambda archive: list(archive))
    word_counts = books.map(lambda book: len(list(book.words())))
    result = [books.count(), word_counts.reduce(add)]
    return {"books": result[0], "words": result[1]}
