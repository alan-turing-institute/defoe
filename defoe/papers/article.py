"""
Object model representation of an article of a newspaper represented
as an XML document.

The XML document can conform to the following schemas:

* British Library Newspapers
* Times Digital Archive

Or newspapers conforming to the following DTDs:

* bl_ncnp_issue_apex.dtd
* GALENP.dtd
* nccoissue.dtd
* LTO_issue.md
"""


class Article(object):
    """
    Object model representation of an article of a newspaper
    represented as an XML document.
    """

    def __init__(self, article_tree, filename):
        """
        Constructor.

        :param article_tree: article XML
        :type article_tree: lxml.etree._Element
        :param filename: file from which the article XML was extracted
        :type: filename: str or unicode
        """
        self.article_tree = article_tree
        self.filename = filename
        self.quality = self.article_tree.xpath('ocr/text()')
        if not self.quality:
            self.quality = None
        elif len(self.quality) == 1:
            self.quality = float(self.quality[0])
        else:
            self.quality = None
        self.title = self.article_tree.xpath('text/text.title/p/wd/text()')
        self.preamble = self.article_tree.xpath(
            'text/text.preamble/p/wd/text()')
        self.content = self.article_tree.xpath('text/text.cr/p/wd/text()')
        self.article_id = ""
        article_id = self.article_tree.xpath('id/text()')
        if article_id:
            self.article_id = str(article_id[0])
        self.page_ids = []
        pi_text = self.article_tree.xpath('pi/text()')
        splitter = None
        if pi_text:
            if "_" in pi_text[0]:
                splitter = "_"
            elif "-" in pi_text[0]:
                splitter = "-"
            if splitter:
                for page_id in pi_text:
                    self.page_ids.append(page_id.split(splitter)[-1])

    @property
    def words(self):
        """
        Get the full text of the article - the title, preamble and
        content - as a list of strings.

        :return: full text
        :rtype: list(str or unicode)
        """
        return self.title + self.preamble + self.content

    @property
    def words_string(self):
        """
        Get the full text of the article - the title, preamble and
        content - as a single string, concatenated by spaces and with
        hyphenation removed.

        Note: merging hyphenated words may cause problems with
        subordinate clauses e.g. "The sheep - the really aloud one -
        had just entered my office".

        :return: full text
        :rtype: str or unicode
        """
        return ' '.join(self.words).replace(' - ', '')

    @property
    def title_string(self):
        """
        Get the title as as a single string, concatenated by spaces
    and with hyphenation removed.

        Note: merging hyphenated words may cause problems with
        subordinate clauses e.g. "The sheep - the really aloud one -
        had just entered my office".

        :return: full text
        :rtype: str or unicode
        """
        return ' '.join(self.title).replace(' - ', '')
