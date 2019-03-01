"""
Object model representation of an XML document.
"""

import os.path
from lxml import etree

from defoe.spark_utils import open_stream


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
        self.root_element = str(self.document_tree.getroot().tag)
        self.doc_type = str(self.document_tree.docinfo.doctype)

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
