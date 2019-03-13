"""
Gets metadata about an XML document.
"""


def do_query(documents, config_file=None, logger=None):
    """
    Gets metadata about an XML document.

    Returns result of form:

        [
            <FILENAME>:
            {
                doctype: <DOCTYPE>,
                namespaces: {<TAG>: <URL>, <TAG>: <URL>, ...},
                no_ns_schema_location: <URL> | None,
                root: <ROOT_ELEMENT>,
                schema_locations: [<URL>, <URL>, ...] | None,
                size: <FILE_SIZE>
            },
            ...
        ]

    :param documents: RDD of defoe.generic_xml.document.Document
    :type documents: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: metadata about the document
    :rtype: dict
    """
    metadata = documents.map(
        lambda document:
        (
            document.filename,
            {
                "size": document.filesize,
                "doctype": document.doc_type,
                "root": document.root_element_tag,
                "namespaces": document.namespaces,
                "schema_locations": document.schema_locations,
                "no_ns_schema_location": document.no_ns_schema_location
            }
        )
    )
    metadata = metadata.collect()
    return metadata
