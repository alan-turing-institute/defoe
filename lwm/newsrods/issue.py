"""
Object module representation of XML issue of newspaper.
"""

from datetime import datetime
from logging import getLogger
from lxml import etree

from newsrods.article import Article


class Issue(object):
    """
    Object module representation of XML issue of newspaper.
    """

    def __init__(self, stream):
        self.logger = getLogger('py4j')
        # Try hard to parse the file, even if it looks like this:
        # <wd pos="1664,5777,2052,5799">Bart,OwnerndPetitioner.Take/wd>
        parser = etree.XMLParser(recover=True)
        try:
            self.tree = etree.parse(stream, parser)
        except etree.XMLSyntaxError as error:
            self.logger.error('Error when parsing: %s',
                              error.msg)
            self.tree = None
            self.issue = ''
            self.articles = []
            self.date = datetime.now()
            self.page_count = 0
            self.day_of_week = ''
            raise error
        # DTD says there's only one issue element
        # Note there are two different DTDs:
        # GALENP: /GALENP/*/issue/page/article/text/*/p/wd
        # LTO: /issue/article/text/*/p/wd
        try:
            self.issue = self.single_query('.//issue')
        except IndexError:
            self.issue = self.single_query('/issue')

        self.articles = [Article(article)
                         for article in self.query('.//article')]
        raw_date = self.single_query('//pf/text()')
        if raw_date:
            self.date = datetime.strptime(raw_date, '%Y%m%d')
        else:
            self.date = None
        try:
            self.page_count = int(self.single_query('//ip/text()'))
        except Exception as error:
            self.logger.error('Failed to get page count: %s', error)
            self.page_count = 0

        self.day_of_week = self.single_query('//dw/text()')

    def query(self, query):
        if not self.tree:
            return []
        try:
            return self.tree.xpath(query)
        except AssertionError:
            return []

    def single_query(self, query):
        result = self.query(query)
        if not result:
            return None
        try:
            return str(result[0])
        except UnicodeEncodeError:
            return unicode(result[0])

    def __getitem__(self, index):
        return self.articles(index)

    def __iter__(self):
        # Iterate through all the articles
        for article in self.articles:
            yield article

    def images(self):
        # Iterate through all the pictures' metadata
        # (Size, caption...)
        for _, image in self.scan_images():
            yield image
