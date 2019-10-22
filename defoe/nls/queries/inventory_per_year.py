"""
Get the editions per year.
"""


def do_query(archives, config_file=None, logger=None, context=None):
    """
    Iterate through archives and get the title and editions per year
    Returns result of form:

    { <YEAR>: [ (title, edition), (title, edition)] }


    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: Title and editions per year
    :rtype: dict
    """
    # [(year, title, edition)]
    documents = archives.flatMap(
        lambda archive: [(document.year, document.title, document.edition) for document in list(archive)])
    doc_years = documents.map(lambda document: (document[0], (document[1], document[2])))

    # [(year, ("title", "edition")), ...]
    # =>
    # [(year, [( title, edition ...),...)]
    result = doc_years \
        .groupByKey() \
        .map(lambda year_context:
             (year_context[0], list(year_context[1]))) \
        .collect()
    return result

     
