"""
defoe.papers.article.Article tests.
"""

from unittest import TestCase

from defoe.papers.issue import Issue
from defoe.file_utils import get_path
from defoe.test.papers import fixtures


class TestArticle(TestCase):
    """
    defoe.papers.article.Article tests.
    """

    def setUp(self):
        """
        Load the standard test file
        """
        self.filename = get_path(fixtures, '1912_11_10.xml')
        issue = Issue(self.filename)
        self.article = issue.articles[0]

    def test_filename(self):
        """
        Check that the filename is correct.
        """
        self.assertEqual(self.filename, self.article.filename)

    def test_words_in_article(self):
        """
        Check that the article length is correct.
        """
        self.assertEqual(7, len(self.article.words))

    def test_ocr_quality(self):
        """
        Make sure that the OCR quality is read.
        """
        self.assertEqual(0, self.article.quality)

    def test_article_id(self):
        """
        Test that the article ID is correct.
        """
        self.assertEqual('NID123-1912-1110-0001-001',
                         self.article.article_id)

    def test_page_ids(self):
        """
        Test that the page IDs are correct.
        """
        self.assertEqual(1, len(self.article.page_ids))
        self.assertEqual("0001", self.article.page_ids[0])
