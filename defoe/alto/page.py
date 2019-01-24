"""
Object model representation of XML page.
"""

from lxml import etree


class Page(object):
    """
    Object model representation of XML page.
    """

    words_path = etree.XPath('//String/@CONTENT')
    strings_path = etree.XPath('//String')
    images_path = etree.XPath('//GraphicalElement')
    page_path = etree.XPath('//Page')

    def __init__(self, document, code, source=None):
        if not source:
            source = document.archive.open_page(document.code, code)
        self.code = code
        self.tree = etree.parse(source)
        self.page_element = self.single_query(Page.page_path)
        self.width = int(self.page_element.get("WIDTH"))
        self.height = int(self.page_element.get("HEIGHT"))
        self.bwords = None
        self.bstrings = None
        self.bimages = None

    def query(self, query):
        return query(self.tree)

    def single_query(self, query):
        result = self.query(query)
        if not result:
            return None
        return result[0]

    @property
    def words(self):
        if not self.bwords:
            self.bwords = list(map(unicode, self.query(Page.words_path)))
        return self.bwords

    @property
    def strings(self):
        if not self.bstrings:
            self.bstrings = self.query(Page.words_path)
        return self.bstrings

    @property
    def images(self):
        if not self.bimages:
            self.bimages = self.query(Page.images_path)
        return self.bimages

    @property
    def content(self):
        return ' '.join(self.words)
