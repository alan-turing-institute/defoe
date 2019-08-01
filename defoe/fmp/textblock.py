"""
Object model representation of a page represented as an XML file in
METS/MODS format.
"""


from lxml import etree


class TextBlock(object):
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
    WC_XPATH = etree.XPath('//String/@WC')
    """ XPath query for Word Confidence  content """
    CC_XPATH = etree.XPath('//String/@CC')
    """ XPath query for Caracther Confidence content """
   

    def __init__(self, textblock_tree):
        """
        Constructor.

        """
	self.textblock_tree = textblock_tree
        self.textblock_words = None
        self.textblock_strings = None
        self.textblock_images = None
        self.textblock_wc = None
        self.textblock_cc = None
        self.textblock_shape = None
        self.textblock_coords = None
        self.textblock_id = self.textblock_tree.get("ID")


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
            self.page_words = list(map(unicode, self.query(TextBlock.WORDS_XPATH)))
        return self.page_words
    
    @property
    def wc(self):
        """
        Gets all word confidences (wc)  in page. These are then saved in an attribute,
        so the wc are only retrieved once.

        :return: wc
        :rtype: list(str)
        """
        if not self.page_wc:
            self.page_wc = list(self.query(TextBlock.WC_XPATH))

        return self.page_wc
    
    @property
    def cc(self):
        """
        Gets all character confidences (cc)  in page. These are then saved in an attribute,
        so the cc are only retrieved once.

        :return: cc
        :rtype: list(str)
        """
        if not self.page_cc:
            self.page_cc = list(self.query(TextBlock.CC_XPATH))

        return self.page_cc

    @property
    def strings(self):
        """
        Gets all strings in page. These are then saved in an attribute,
        so the strings are only retrieved once.

        :return: strings
        :rtype: list(lxml.etree._ElementStringResult)
        """
        if not self.page_strings:
            self.page_strings =self.query(TextBlock.STRINGS_XPATH)
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
            self.page_images = self.query(TextBlock.IMAGES_XPATH)
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
