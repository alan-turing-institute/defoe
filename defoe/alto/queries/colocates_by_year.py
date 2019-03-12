"""
Gets colocated words and groups by year.
"""

import os
import yaml

from defoe import query_utils


def do_query(archives, config_file=None, logger=None):
    """
    Gets colocated words and groups by year.

    config_file must be the path to a configuration file with the
    words to be searched for and the maximum number of intervening
    words (a "window"). This file must be a YAML document of form:

        start_word: <WORD>
        end_word: <WORD>
        window: <WINDOW>

    where <WINDOW> is greater than or equal to 0. If omitted then a
    default of 0 is assumed.

    Both colocated words and words in documents are normalized, by
    removing all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <YEAR>:
          [
            {
              "document_id": <DOCUMENT_ID>,
              "place": <PLACE>,
              "publisher": <PUBLISHER>,
              "filename": <FILENAME>
              "matches":
              [
                {
                  "start_page": <PAGE_ID>,
                  "end_page": <PAGE_ID>,
                  "span": [<WORD>, ..., <WORD>]
                },
                ...
              ]
            },
            ...
          ],
          <YEAR>:
          ...
        }

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
    window = 0
    if config_file is not None and\
       os.path.exists(config_file) and\
       os.path.isfile(config_file):
        with open(config_file, "r") as f:
            config = yaml.load(f)
        start_word = query_utils.normalize(config["start_word"])
        end_word = query_utils.normalize(config["end_word"])
        window = config["window"]
        if window < 0:
            raise ValueError('window must be at least 0')

    # [document, ...]
    documents = archives.flatMap(
        lambda archive: [document for document in list(archive)])

    # [(document, matches), ...]
    colocated_words = documents.map(
        lambda document: (document, get_colocates_matches(document,
                                                          start_word,
                                                          end_word,
                                                          window)))
    # [(document, matches), ...]
    colocated_words = colocated_words.filter(
        lambda document_matches: len(document_matches[1]) > 0)

    # [(document, matches), ...]
    # =>
    # [(year, {"title": title, ...}), ...]
    matching_docs = colocated_words.map(
        lambda document_matches:
        (
            document_matches[0].year,
            {
                "title": document_matches[0].title,
                "place": document_matches[0].place,
                "publisher": document_matches[0].publisher,
                "document_id": document_matches[0].code,
                "filename": document_matches[0].archive.filename,
                "matches": document_matches[1]
            }
        )
    )

    # [(year, {"title": title, ...}), ...]
    # =>
    # [(year, [{"title": title, ...], {...}), ...)]
    result = matching_docs \
        .groupByKey() \
        .map(lambda year_context:
             (year_context[0], list(year_context[1]))) \
        .collect()
    return result


def get_colocates_matches(document, start_word, end_word, window=0):
    """
    Get pages within a document that include colocates, one word
    followed by another word, with 0 or more intervening words.

    For each span of text, '<START_WORD> ... <END_WORD>', delimited by
    the colocates, a dictionary of the following form is included in
    the list returned:

        {
          "start_page": <PAGE_CODE>,
          "end_page": <PAGE_CODE>,
          "span": [<START_WORD>, ..., <END_WORD>]
        }

    :param document: document
    :type document: defoe.alto.document.Document
    :param start_word: start_word colocate
    :type start_word: str or unicode
    :param end_word: end_word colocate
    :type end_word: str or unicode
    :return: list of dicts
    :rtype: list(dict)
    """
    start_page = None
    span = []
    span_length = 0
    matches = []
    window_plus_colocates = window + 2
    for page, word in document.scan_words():
        normalized_word = query_utils.normalize(word)
        if not normalized_word:
            continue
        if normalized_word == start_word:
            start_page = page
            span = []
            span_length = 0
        if start_page is not None:
            span.append(normalized_word)
            span_length += 1
            if span_length > window_plus_colocates:
                start_page = None
                span = []
                span_length = 0
                continue
            if normalized_word == end_word:
                matches.append({"start_page": str(start_page.code),
                                "end_page": str(page.code),
                                "span": span})
                start_page = None
                span = []
                span_length = 0
    return matches
