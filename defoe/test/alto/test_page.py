"""
defoe.alto.page.Page tests.
"""

from unittest import TestCase

from defoe.alto.page import Page
from defoe.test import get_path
from defoe.test.alto import fixtures


class TestPage(TestCase):
    """
    defoe.alto.page.Page tests.
    """

    def setUp(self):
        source = get_path(fixtures, '000000037_000005.xml')
        self.page = Page(None, None, source)

    def test_content(self):
        self.assertTrue("BEFORE YOU BUY" in self.page.content)
