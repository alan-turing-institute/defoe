"""
Object model representation of an issue of a newspaper represented as
an XML document.

The XML document can conform to the following schemas:

* British Library Newspapers
* Times Digital Archive

Or newspapers conforming to the following DTDs:

* bl_ncnp_issue_apex.dtd
* GALENP.dtd
* nccoissue.dtd
* LTO_issue.md
"""

from datetime import datetime
from lxml import etree

from defoe.papers.article import Article
from defoe.spark_utils import open_stream


class Issue(object):
    """
    Object model representation of an issue of a newspaper represented
    as an XML document.
    """

    def __init__(self, filename):
        """
        Constructor. If the filename cannot be parsed into valid XML
        an empty document is created.

        :param filename: XML filename
        :type: filename: str or unicode
        """
        self.filename = filename
        stream = open_stream(self.filename)

        self.issue_tree = None
        self.issue = ''
        self.newspaper_id = ''
        self.articles = []
        self.date = datetime.now()
        self.page_count = 0
        self.day_of_week = ''
        # Attempt to parse the file, even if its XML is invalid e.g:
        # <wd ...>.../wd>
        parser = etree.XMLParser(recover=True)
        self.issue_tree = etree.parse(stream, parser)

        has_issue = len(self.query("..//issue")) > 0
        if not has_issue:
            raise Exception("Missing 'issue' element")

        self.issue = self.single_query('.//issue')

        # bl_ncnp_issue_apex.dtd, GALENP.dtd, nccoissue.dtd
        newspaper_id = self.single_query('//issue/id/text()')
        if newspaper_id is None:
            # LTO_issue.md
            newspaper_id = self.single_query('//issue/metadatainfo/PSMID/text()')
        if newspaper_id is not None:
            self.newspaper_id = newspaper_id

        self.articles = [Article(article, self.filename)
                         for article in self.query('.//article')]

        # bl_ncnp_issue_apex.dtd, GALENP.dtd, LTO_issue.dtd
        raw_date = self.single_query('//pf/text()')
        if raw_date is None:
            # nccoissue.dtd
            raw_date = self.single_query('//da/searchableDateStart/text()')
        if raw_date:
            self.date = datetime.strptime(raw_date, '%Y%m%d')
        else:
            self.date = None

        try:
            self.page_count = int(self.single_query('//ip/text()'))
        except Exception:
            pass

    def query(self, query):
        """
        Run XPath query.

        :param query: XPath query
        :type query: str or unicode
        :return: list of query results or an empty list if the object
        represents an empty document or any errors arose
        :rtype: list(lxml.etree.<MODULE>) (depends on query)
        """
        if not self.issue_tree:
            return []
        try:
            return self.issue_tree.xpath(query)
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
        :rtype: defoe.alto.article.Article
        """
        return self.articles(index)

    def __iter__(self):
        """
        Iterate over articles.

        :return: Article object
        :rtype: defoe.alto.article.Article
        """
        for article in self.articles:
            yield article
