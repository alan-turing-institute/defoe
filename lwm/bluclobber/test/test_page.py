"""
bluclobber.page.Page tests.
"""

from unittest import TestCase

from bluclobber.page import Page
from bluclobber.test.fixtures import get_path


class TestPage(TestCase):
    """
    bluclobber.page.Page tests.
    """

    def setUp(self):
        source = get_path('page.xml')
        self.page = Page(None, None, source)

    def test_content(self):
        self.assertTrue("LOVE THE AVENGER" in self.page.content)
