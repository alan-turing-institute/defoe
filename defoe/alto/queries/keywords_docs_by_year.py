"""
Gets information on documents in which keywords occur and groups by year.
"""

from defoe import query_utils


def do_query(archives, config_file=None, logger=None):
    """
    Gets information on documents in which keywords occur  and groups
    by year.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        <YEAR>:
        - { "title": <TITLE>,
            "place": <PLACE>,
            "publisher": <PUBLISHER>,
            "page_number": <PAGE_NUMBER>,
            "content": <PAGE_CONTENT>,
            "word": <WORD> }
        - { ... }
        ...
        <YEAR>:
        ...

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by year
    :rtype: dict
    """
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.normalize(word) for word in list(f)]
    # [(year, document), ...]
    documents = archives.flatMap(
        lambda archive: [(document.year, document) for document in list(archive)])

    # [(year, document, page, word), ...]
    words = documents.flatMap(
        lambda year_document: [
            (year_document[0],
             year_document[1],
             page,
             query_utils.normalize(word))
            for (page, word) in year_document[1].scan_words()
        ])

    # [(year, document, page, word), ...]
    filtered_words = words.filter(
        lambda year_document_page_word: year_document_page_word[3] in keywords)

    # [(year, document, page, word), ...]
    # =>
    # [(year, {"title": title, ...}), ...]
    matching_docs = filtered_words.map(
        lambda year_document_page_word:
        (year_document_page_word[0],
         {"title": year_document_page_word[1].title,
          "place": year_document_page_word[1].place,
          "publisher": year_document_page_word[1].publisher,
          "page_number": year_document_page_word[2].code,
          "content": year_document_page_word[2].content,
          "word": year_document_page_word[3]}))

    # [(year, {"title": title, ...}), ...]
    # =>
    # [(year, [{"title": title, ...], {...}), ...)]
    result = matching_docs \
        .groupByKey() \
        .map(lambda year_context:
             (year_context[0], list(year_context[1]))) \
        .collect()
    return result