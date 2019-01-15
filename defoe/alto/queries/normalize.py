"""
Counts total number of documents, pages, words. This can be useful if
wanting to see how the average number of documents, pages and words
change over time.

The result is of form, for example:

    YEAR: [DOCUMENTS, PAGES, WORDS]
    YEAR: [DOCUMENTS, PAGES, WORDS]
    ...
"""


def do_query(archives, data_file=None, logger=None):
    """
    Counts total number of documents, pages, words.
    """
    documents = archives.flatMap(lambda archive: list(archive))

    counts = documents.map(lambda document:
                           (document.year,
                            (1, document.pages, len(list(document.words())))))

    result = counts \
        .reduceByKey(lambda x, y:
                     tuple(i + j for i, j in zip(x, y))) \
        .map(lambda year_data: (year_data[0], list(year_data[1]))) \
        .collect()
    return result
