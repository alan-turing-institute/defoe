"""
Object model representation of a collection of articles from
New Zealand Papers Past represented as an XML document.
"""

from lxml import etree

from defoe.nzpp.article import Article
from defoe.spark_utils import open_stream


class Articles(object):
    """
    Object model representation of a collaction of articles from
    New Zealand Papers Past represented as an XML document.
    """

    def __init__(self, filename):
        """
        Constructor.

        :param filename: XML filename
        :type: filename: str or unicode
        """
        self.filename = filename
        stream = open_stream(self.filename)
        parser = etree.XMLParser(recover=True)
        self.xml_tree = etree.parse(stream, parser)
        self.articles = [Article(article, self.filename)
                         for article in self.query('.//result')]

    def query(self, query):
        """
        Run XPath query.

        :param query: XPath query
        :type query: str or unicode
        :return: list of query results or an empty list if the object
        represents an empty document or any errors arose
        :rtype: list(lxml.etree.<MODULE>) (depends on query)
        """
        if not self.xml_tree:
            return []
        try:
            return self.xml_tree.xpath(query)
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

    def __getitem__(self, index):
        """
        Given an article index, return the requested article.

        :param index: article index
        :type index: int
        :return: Article object
        :rtype: defoe.nzpp.article.Article
        """
        return self.articles(index)

    def __iter__(self):
        """
        Iterate over articles.

        :return: Article object
        :rtype: defoe.nzpp.article.Article
        """
        for article in self.articles:
            yield article
