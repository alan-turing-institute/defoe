"""
Gets contextual information about the occurences of words and
group by year.

The query expects a file with a list of the words to search for, one
per line.

Words are normalized, by removing all 'a-z|A-Z' characters before
comparing with the list of words to search for.

The result is of form, for example:

    YEAR:
    - { "title": TITLE,
        "place": PLACE,
        "publisher": PUBLISHER,
        "page": PAGE,
        "text": TEXT,
        "word": WORD }
    - { ... }
    ...
    YEAR:
    ...
"""

import utils


def do_query(archives, words_file, logger=None):
    """
    Gets contextual information about the occurences of words
    and group by year.

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
            (year_book[0], year_book[1], page, utils.normalize(word))
            for (page, word) in year_book[1].scan_words()
        ])

    filtered_words = words.filter(
        lambda year_book_page_word: year_book_page_word[3] in search_words)

    words_and_context = filtered_words.map(
        lambda year_book_page_word:
        (year_book_page_word[0],
         {"title": year_book_page_word[1].title,
          "place": year_book_page_word[1].place,
          "publisher": year_book_page_word[1].publisher,
          "page": year_book_page_word[2].code,
          "text": year_book_page_word[2].content,
          "word": year_book_page_word[3]}))

    result = words_and_context \
        .groupByKey() \
        .map(lambda year_context:
             (year_context[0], list(year_context[1]))) \
        .collect()
    return result
