"""
Gets contextual information about the occurences of words and
group by word.

The query expects a file with a list of the words to search for, one
per line.

Words are normalized, by removing all 'a-z|A-Z' characters before
comparing with the list of words to search for.

The result is of form, for example:

    WORD:
    - { "title": TITLE,
        "place": PLACE,
        "publisher": PUBLISHER,
        "page": PAGE,
        "text": TEXT,
        "year": YEAR }
    - { ... }
    ...
    WORD:
    ...
"""

import utils


def do_query(archives, words_file, logger=None):
    """
    Gets contextual information about the occurences of words
    and group by word.

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
        lambda archive: [book for book in list(archive)])

    words = books.flatMap(
        lambda book: [
            (book, page, utils.normalize(word))
            for (page, word) in book.scan_words()
        ])

    filtered_words = words.filter(
        lambda book_page_word: book_page_word[2] in search_words)

    words_and_context = filtered_words.map(
        lambda book_page_word:
        (book_page_word[2],
         {"title": book_page_word[0].title,
          "place": book_page_word[0].place,
          "publisher": book_page_word[0].publisher,
          "page": book_page_word[1].code,
          "text": book_page_word[1].content,
          "year": book_page_word[0].year}))

    result = words_and_context \
        .groupByKey() \
        .map(lambda word_context:
             (word_context[0], list(word_context[1]))) \
        .collect()
    return result
