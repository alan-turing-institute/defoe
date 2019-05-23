"""
defoe.papers.article.Article tests.
"""

from unittest import TestCase


class TestArticle(TestCase):
    """
    defoe.papers.article.Article tests.
    """

    __test__ = False

    def test_filename(self):
        """
        Tests Article.filename attribute holds the expected filename.
        """
        self.assertEqual(self.filename, self.article.filename)

    def test_article_id(self):
        """
        Tests Article.article_id attribute holds the expected article ID>
        """
        self.assertEqual(self.article_id, self.article.article_id)

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

    def test_words_string(self):
        """
        Tests Article.words_string property holds the expected
        content.
        """
        words = self.article.words_string
        self.assertEqual("Article 1 Title A B C D E F",
                         words)

    def test_title_string(self):
        """
        Tests Article.title_string property holds the expected
        content.
        """
        title = self.article.title_string
        self.assertEqual("Article 1 Title", title)

    def test_page_ids(self):
        """
        Tests Article.page_ids holds the expected number of page IDs
        and that these are as expected.
        """
        page_ids = self.article.page_ids
        self.assertEqual(1, len(page_ids))
        self.assertTrue(self.page_id in page_ids)
