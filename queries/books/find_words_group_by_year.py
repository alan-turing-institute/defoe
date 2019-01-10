"""
Counts the number of occurrences of words per-year and groups by
year.

The query expects a file with a list of the words to search for, one
per line.

Words are normalized, by removing all 'a-z|A-Z' characters before
comparing with the list of words to search for.

The result is of form, for example:

    YEAR:
    - [WORD, N]
    - [WORD, N]
    - ...
    YEAR:
    ...

Only words that occur one or more times are returned.
"""

from operator import add

import utils


def do_query(archives, words_file, logger=None):
    """
    Counts the number of occurrences of words per-year and groups by
    year.

    @param archives: Archives holding Books
    @type archives: pyspark.rdd.PipelinedRDD with Archives.
    @param words_file: File with list of words to search for,
    one per line
    @type words_file: str or unicode
    @param logger: Logger
    """
    search_words = []
    with open(words_file, "r") as f:
        search_words = [word.strip() for word in list(f)]

    books = archives.flatMap(
        lambda archive: [(book.year, book) for book in list(archive)])

    words = books.flatMap(
        lambda year_book: [
            ((year_book[0], utils.normalize(word)), 1)
            for (_, word) in year_book[1].scan_words()
        ])

    num_matches = words.filter(
        lambda yearword_count: yearword_count[0][1] in search_words)

    result = num_matches \
        .reduceByKey(add) \
        .map(lambda yearword_count:
             (yearword_count[0][0],
              (yearword_count[0][1], yearword_count[1]))) \
        .groupByKey() \
        .map(lambda year_wordcount:
             (year_wordcount[0], list(year_wordcount[1]))) \
        .collect()
    return result
