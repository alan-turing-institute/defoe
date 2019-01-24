"""
defoe.alto.page.Page tests.
"""

from unittest import TestCase

from defoe.alto.page import Page
from defoe.file_utils import get_path
from defoe.test.alto import fixtures


class TestPage(TestCase):
    """
    defoe.alto.page.Page tests.
    """

    def setUp(self):
        """
        Creates Page from test file fixtures/000000037_000005.xml.
        """
        source = get_path(fixtures, '000000037_000005.xml')
        self.page = Page(None, None, source)

    def test_words_count(self):
        """
        Tests Page.words property returns expected number of words.
        """
        self.assertEqual(52, len(self.page.words))

    def test_words_words(self):
        """
        Tests Page.words property includes expected words.
        """
        words = self.page.words
        for word in ["BEFORE", "YOU", "BUY"]:
            self.assertTrue(word in words)

    def test_strings_count(self):
        """
        Tests Page.strings property returns expected number of strings.
        """
        self.assertEqual(52, len(self.page.strings))

    def test_images_count(self):
        """
        Tests Page.strings property returns expected number of images.
        """
        self.assertEqual(0, len(self.page.images))

    def test_content(self):
        """
        Tests Page.content property returns text which includes an
        expected phrase.
        """
        self.assertTrue("BEFORE YOU BUY" in self.page.content)
