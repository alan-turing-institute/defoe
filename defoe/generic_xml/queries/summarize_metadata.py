"""
Gets metadata about an XML document and counts frequences of each type
of metadata.
"""

from operator import add


def do_query(documents, config_file=None, logger=None):
    """
    Gets metadata about an XML document and counts frequences of each
    type of metadata.

    Returns result of form:

        {
            "doc_type": { <DOCTYPE>: <COUNT>, ... },
            "root": { <ROOT_ELEMENT>: <COUNT>, ... },
            "namespace": { <NAMESPACE>: <COUNT>, ... },
            "schemaLocation": { <URL>: <COUNT>, ... },
            "noNsSchemaLocation": { <URL>: <COUNT>, ...}
        }

    :param documents: RDD of defoe.generic_xml.document.Document
    :type documents: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: metadata about the document
    :rtype: dict
    """
    doc_types = documents.map(lambda document:
                              (document.doc_type, 1))
    doc_type_counts = doc_types. \
        reduceByKey(add). \
        collect()
    root_elements = documents.map(lambda document:
                                  (document.root_element_tag, 1))
    root_element_counts = root_elements. \
        reduceByKey(add). \
        collect()
    namespaces = documents.flatMap(lambda document:
                                   get_namespaces(document))
    namespace_counts = namespaces. \
        reduceByKey(add). \
        collect()
    schema_locations = documents.flatMap(lambda document:
                                         get_schema_locations(document))
    schema_location_counts = schema_locations. \
        reduceByKey(add). \
        collect()
    no_ns_locations = documents.map(lambda document:
                                    (document.no_ns_schema_location, 1))
    no_ns_location_counts = no_ns_locations. \
        reduceByKey(add). \
        collect()
    result = {
        "doc_type": doc_type_counts,
        "root": root_element_counts,
        "namespace": namespace_counts,
        "schemaLocation": schema_location_counts,
        "noNsSchemaLocation": no_ns_location_counts
    }
    return result


def get_namespaces(document):
    """
    Extract namespaces from a document.

    :param document: defoe.generic_xml.document.Document
    :type document: defoe.generic_xml.document.Document
    :return: list of (URL, 1) for each namespace URL in the
    document
    :rtype: list(tuple(str or unicode, 1))
    """
    return [(tag_url[1], 1) for tag_url in list(document.namespaces.items())]


def get_schema_locations(document):
    """
    Extract schema locations from a document.

    :param document: defoe.generic_xml.document.Document
    :type document: defoe.generic_xml.document.Document
    :return: list of (URL, 1) for each schema location URL in the
    document
    :rtype: list(tuple(str or unicode, 1))
    """
    return [(location, 1) for location in document.schema_locations]
