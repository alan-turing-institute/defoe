"""
Object model representation of a page represented as an XML file in
METS/MODS format.
"""


from lxml import etree


class Page(object):
    """
    Object model representation of a page represented as an XML file
    in METS/MODS format.
    """

    WORDS_XPATH = etree.XPath('//String/@CONTENT')
    """ XPath query for String content """
    STRINGS_XPATH = etree.XPath('//String')
    """ XPath query for String elements """
    IMAGES_XPATH = etree.XPath('//GraphicalElement')
    """ XPath query for Graphical Element """
    PAGE_XPATH = etree.XPath('//Page')
    """ XPath query for Page """

    def __init__(self, document, code, source=None):
        """
        Constructor.

        :param document: Document object corresponding to document to
        which this page belongs
        :type document: defoe.alto.document.Document
        :param code: identifier for this page within an archive
        :type code: str or unicode
        :param source: stream. If None then an attempt is made to
        open the file holding the page via the given "document"
        :type source: zipfile.ZipExt or another file-like object
        """
        if not source:
            source = document.archive.open_page(document.code, code)
        self.code = code
        self.tree = etree.parse(source)
        self.page_tree = self.single_query(Page.PAGE_XPATH)
        self.width = int(self.page_tree.get("WIDTH"))
        self.height = int(self.page_tree.get("HEIGHT"))
        self.pc = self.page_tree.get("PC")
        self.page_words = None
        self.page_strings = None
        self.page_images = None

    def query(self, xpath_query):
        """
        Run XPath query.

        :param xpath_query: XPath query
        :type xpath_query: lxml.etree.XPath
        :return: list of query results or None if none
        :rtype: list(lxml.etree.<MODULE>) (depends on query)
        """
        return xpath_query(self.tree)

    def single_query(self, xpath_query):
        """
        Run XPath query and return first result.

        :param xpath_query: XPath query
        :type xpath_query: lxml.etree.XPath
        :return: query result or None if none
        :rtype: lxml.etree.<MODULE> (depends on query)
        """
        result = self.query(xpath_query)
        if not result:
            return None
        return result[0]

    @property
    def words(self):
        """
        Gets all words in page. These are then saved in an attribute,
        so the words are only retrieved once.

        :return: words
        :rtype: list(str or unicode)
        """
        if not self.page_words:
            self.page_words = list(map(unicode, self.query(Page.WORDS_XPATH)))
        return self.page_words

    @property
    def strings(self):
        """
        Gets all strings in page. These are then saved in an attribute,
        so the strings are only retrieved once.

        :return: strings
        :rtype: list(lxml.etree._ElementStringResult)
        """
        if not self.page_strings:
            self.page_strings = self.query(Page.STRINGS_XPATH)
        return self.page_strings

    @property
    def images(self):
        """
        Gets all images in page. These are then saved in an attribute,
        so the images are only retrieved once.

        :return: images
        :rtype: list(lxml.etree._Element)
        """
        if not self.page_images:
            self.page_images = self.query(Page.IMAGES_XPATH)
        return self.page_images

    @property
    def content(self):
        """
        Gets all words in page and contatenates together using ' ' as
        delimiter.

        :return: content
        :rtype: str or unicode
        """
        return ' '.join(self.words)
