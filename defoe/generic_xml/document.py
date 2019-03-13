"""
Object model representation of an XML document.
"""

import os.path
from lxml import etree

from defoe.spark_utils import open_stream


XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
SCHEMA_LOCATION = etree.QName(XSI_NS, "schemaLocation")
NO_NS_SCHEMA_LOCATION = etree.QName(XSI_NS, "noNamespaceSchemaLocation")


class Document(object):
    """
    Object model representation of an XML document.
    """

    def __init__(self, filename):
        """
        Constructor.

        :param filename: XML filename
        :type: filename: str or unicode
        """
        self.filename = filename
        self.filesize = os.path.getsize(filename)

        stream = open_stream(self.filename)
        self.document_tree = None
        parser = etree.XMLParser()
        self.document_tree = etree.parse(stream, parser)
        self.root_element = self.document_tree.getroot()
        self.root_element_tag = str(self.root_element.tag)
        self.doc_type = str(self.document_tree.docinfo.doctype)
        self.namespaces = self.root_element.nsmap
        self.schema_locations = self.root_element.get(
            SCHEMA_LOCATION.text)
        if self.schema_locations is not None:
            self.schema_locations = self.schema_locations.split(" ")
        else:
            self.schema_locations = []
        self.no_ns_schema_location = self.root_element.get(
            NO_NS_SCHEMA_LOCATION.text)

    def query(self, query):
        """
        Run XPath query.

        :param query: XPath query
        :type query: str or unicode
        :return: list of query results or an empty list if the object
        represents an empty document or any errors arose
        :rtype: list(lxml.etree.<MODULE>) (depends on query)
        """
        if not self.document_tree:
            return []
        try:
            return self.document_tree.xpath(query)
        except AssertionError:
            return []

    def single_query(self, query):
        """
        Run XPath query and return first result.

        :param query: XPath query
        :type query: str or unicode
        :return: query results or None if the object represents an
        empty document or any errors arose
        :rtype: str or unicode
        """
        result = self.query(query)
        if not result:
            return None
        try:
            return str(result[0])
        except UnicodeEncodeError:
            return unicode(result[0])
