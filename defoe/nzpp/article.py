"""
Object model representation of an article in a New Zealand Papers Past
newspaper represented as an XML document.
"""

from datetime import datetime


class Article(object):
    """
    Object model representation of an article in a New Zealand Papers
    Past newspaper represented as an XML document.
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
        # <title> tag is present twice in each article record as a
        # duplicate of a kind. findtext() returns only the
        # occurrence.
        self.title = self.article_tree.findtext('title').split(' ')
        # Article text is a single element, split on space.
        self.content = self.article_tree.findtext('fulltext').split(' ')

        raw_date = self.article_tree.findtext('display-date')
        self.date = datetime.strptime(raw_date, '%d-%m-%Y')

        # Newspaper name is analogous to publisher.
        self.paper_name = self.article_tree.findtext('publisher/publisher')
        # Article type.
        self.article_type = self.article_tree.findtext('dnz-type')

    @property
    def words(self):
        """
        Get the full text of the article - the title and content - as
        a list of strings.

        :return: full text
        :rtype: list(str or unicode)
        """
        return self.title + self.content

    @property
    def words_string(self):
        """
        Get the full text of the article - the title and content - as
        a single string, concatenated by spaces and with hyphenation
        removed.

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
