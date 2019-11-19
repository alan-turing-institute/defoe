"""
Object model representation of a textblock represented as an XML file in
METS/MODS format.
"""


from lxml import etree


class TextBlock(object):
    """
    Object model representation of a textblock represented as an XML file
    in METS/MODS format.
    """

    STRINGS_XPATH = 'TextLine/String'
    """ Query for String elements """
    WC_XPATH = 'TextLine/String/@WC'
    """ Query for Word Confidence  content """
    CC_XPATH = 'TextLine/String/@CC'
    """ query for Caracther Confidence content """
    WORDS_XPATH = 'TextLine/String/@CONTENT'
    """ query for word content """

    def __init__(self, textblock_tree, document_code, page_code):
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
        self.textblock_page_area = None
        self.textblock_id = self.textblock_tree.get("ID")
        self.page_name = document_code + '_' + page_code + '.xml'


    @property
    def words(self):
        """
        Gets all words in textblock. These are then saved in an attribute,
        so the words are only retrieved once.

        :return: words
        :rtype: list(str or unicode)
        """
        if not self.textblock_words:
            self.textblock_words = list(map(str, self.textblock_tree.xpath(TextBlock.WORDS_XPATH)))
        return self.textblock_words
    
    @property
    def wc(self):
        """
        Gets all word confidences (wc)  in textblock. These are then saved in an attribute,
        so the wc are only retrieved once.

        :return: wc
        :rtype: list(str)
        """
        if not self.textblock_wc:
            self.textblock_wc = list(self.textblock_tree.xpath(TextBlock.WC_XPATH))
        return self.textblock_wc
    
    @property
    def cc(self):
        """
        Gets all character confidences (cc)  in textblock. These are then saved in an attribute,
        so the cc are only retrieved once.

        :return: cc
        :rtype: list(str)
        """
        if not self.textblock_cc:
            self.textblock_cc = list(self.textblock_tree.xpath(TextBlock.CC_XPATH))

        return self.textblock_cc

    @property
    def strings(self):
        """
        Gets all strings in textblock. These are then saved in an attribute,
        so the strings are only retrieved once.

        :return: strings
        :rtype: list(lxml.etree._ElementStringResult)
        """
        if not self.textblock_strings:
            self.textblock_strings =self.textblock_tree.xpath(TextBlock.STRINGS_XPATH)
        return self.textblock_strings
    

    @property
    def content(self):
        """
        Gets all words in textblock and contatenates together using ' ' as
        delimiter.

        :return: content
        :rtype: str or unicode
        """
        return ' '.join(self.words)

