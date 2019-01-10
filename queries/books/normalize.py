"""
Counts total number of books, pages, words. This can be useful if
wanting to see how the average number of books, pages and words change
over time.

The result is of form, for example:

    YEAR: [BOOKS, PAGES, WORDS]
    YEAR: [BOOKS, PAGES, WORDS]
    ...
"""


def do_query(archives, data_file=None, logger=None):
    """
    Counts total number of books, pages, words.
    """
    books = archives.flatMap(lambda archive: list(archive))

    counts = books.map(lambda book:
                       (book.year, (1, book.pages, len(list(book.words())))))

    result = counts \
        .reduceByKey(lambda x, y:
                     tuple(i + j for i, j in zip(x, y))) \
        .map(lambda year_data: (year_data[0], list(year_data[1]))) \
        .collect()
    return result
