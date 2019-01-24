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
        Creates Issue from test file fixtures/1912_11_10.xml then
        retrieves first Article.
        """
        self.filename = get_path(fixtures, '1912_11_10.xml')
        issue = Issue(self.filename)
        self.article = issue.articles[0]

    def test_filename(self):
        """
        Tests Article.filename attribute holds the expected filename.
        """
        self.assertEqual(self.filename, self.article.filename)

    def test_article_id(self):
        """
        Tests Article.article_id attribute holds the expected article ID>
        """
        self.assertEqual('NID123-1912-1110-0001-001',
                         self.article.article_id)

    def test_quality(self):
        """
        Tests Article.quality attribute holds the expected OCR quality.
        """
        self.assertEqual(0, self.article.quality)

    def test_words(self):
        """
        Tests Article.words attribute holds the expected number of
        words and that the words are as expected:
        """
        words = self.article.words
        self.assertEqual(7, len(words))
        for word in ["Article 1 Title", "A", "B", "C", "D", "E", "F"]:
            self.assertTrue(word in words)

    def test_page_ids(self):
        """
        Tests Article.page_ids holds the expected number of page IDs
        and that these are as expected.
        """
        page_ids = self.article.page_ids
        self.assertEqual(1, len(page_ids))
        self.assertTrue("0001" in page_ids)
