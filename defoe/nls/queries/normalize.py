"""
Counts total number of documents, pages and words per year.

This can be useful if wanting to see how the average number of
documents, pages and words change over time, for example.
"""


def do_query(archives, config_file=None, logger=None):
    """
    Iterate through archives and count total number of documents,
    pages and words per year.

    Returns result of form:

        {
          <YEAR>: [<NUM_DOCUMENTS>, <NUM_PAGES>, <NUM_WORDS>],
          ...
        }

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of documents, pages and words per year
    :rtype: list
    """
    # [archive, archive, ...]
    documents = archives.flatMap(lambda archive: list(archive))
    # [(year, (1, num_pages, num_words)), ...]
    counts = documents.map(lambda document:
                           (document.year,
                            (1, document.num_pages, len(list(document.words())))))
    # [(year, (num_documents, num_pages, num_words)), ...]
    # =>
    # [(year, [num_documents, num_pages, num_words]), ...]
    result = counts \
        .reduceByKey(lambda x, y:
                     tuple(i + j for i, j in zip(x, y))) \
        .map(lambda year_data: (year_data[0], list(year_data[1]))) \
        .collect()
    return result
