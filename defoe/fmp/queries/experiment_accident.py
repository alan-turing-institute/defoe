"""
Gets concordance for keywords and groups by word.
"""

from defoe import query_utils
from defoe.alto.query_utils import get_page_matches


def do_query(archives, config_file=None, logger=None):
    """
    Gets concordance for keywords and groups by word.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <WORD>:
          [
            { "title": <TITLE>,
              "place": <PLACE>,
              "publisher": <PUBLISHER>,
              "page_number": <PAGE_NUMBER>,
              "content": <PAGE_CONTENT>,
              "year": <YEAR>,
              "document_id": <DOCUMENT_ID>,
              "filename": <FILENAME>
            },
            ...
          ],
          <WORD>:
          ...
        }

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by word
    :rtype: dict
    """
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.normalize(word) for word in list(f)]
    # [document, ...]
    documents = archives.flatMap(
        lambda archive: [document for document in list(archive)])

    # [(year, document, page, word), ...]
    filtered_words = documents.flatMap(
        lambda document: get_page_matches(document,
                                          keywords))

    # [(year, document, page, word), ...]
    # =>
    # [(word, {"title": title, ...}), ...]
    matching_docs = filtered_words.map(
        lambda year_document_page_word:
        (year_document_page_word[3],
         {"title": year_document_page_word[1].title,
          "place": year_document_page_word[1].place,
          "publisher": year_document_page_word[1].publisher,
          "page_number": year_document_page_word[2].code,
          "content": year_document_page_word[2].content,
          "year": year_document_page_word[0],
          "document_id": year_document_page_word[1].code,
          "filename": year_document_page_word[1].archive.filename}))

    # [(word, {"title": title, ...}), ...]
    # =>
    # [(word, [{"title": title, ...], {...}), ...)]
    result = matching_docs \
        .groupByKey() \
        .map(lambda year_context:
             (year_context[0], list(year_context[1]))) \
        .collect()
    return result
