"""
defoe.books.page.Page tests.
"""

from unittest import TestCase

from defoe.books.page import Page
from defoe.test.books import fixtures
from defoe.test import get_path


class TestPage(TestCase):
    """
    defoe.books.page.Page tests.
    """

    def setUp(self):
        source = get_path(fixtures, 'page.xml')
        self.page = Page(None, None, source)

    def test_content(self):
        self.assertTrue("LOVE THE AVENGER" in self.page.content)
