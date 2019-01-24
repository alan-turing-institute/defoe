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

from defoe import query_utils


def do_query(archives, words_file, logger=None):
    """
    Gets contextual information about the occurences of words
    and group by year.

    @param archives: Archives holding Documents
    @type archives: pyspark.rdd.PipelinedRDD with Archives.
    @param words_file: File with list of words to search for,
    one per line
    @type words_file: str or unicode
    @param logger: Logger
    """
    search_words = []
    with open(words_file, "r") as f:
        search_words = [word.strip() for word in list(f)]

    documents = archives.flatMap(
        lambda archive: [(document.year, document) for document in list(archive)])

    words = documents.flatMap(
        lambda year_document: [
            (year_document[0], year_document[1], page, query_utils.normalize(word))
            for (page, word) in year_document[1].scan_words()
        ])

    filtered_words = words.filter(
        lambda year_document_page_word: year_document_page_word[3] in search_words)

    words_and_context = filtered_words.map(
        lambda year_document_page_word:
        (year_document_page_word[0],
         {"title": year_document_page_word[1].title,
          "place": year_document_page_word[1].place,
          "publisher": year_document_page_word[1].publisher,
          "page": year_document_page_word[2].code,
          "text": year_document_page_word[2].content,
          "word": year_document_page_word[3]}))

    result = words_and_context \
        .groupByKey() \
        .map(lambda year_context:
             (year_context[0], list(year_context[1]))) \
        .collect()
    return result
