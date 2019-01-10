"""
bluclobber.archive.Archive tests.
"""

from unittest import TestCase

from bluclobber.test.fixtures import open_file
from bluclobber.archive import Archive


class TestArchive(TestCase):
    """
    bluclobber.archive.Archive tests.
    """

    def setUp(self):
        source = open_file('000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(source)

    def test_books(self):
        self.assertEqual(['000000218', '000000037'],
                         list(self.archive.book_codes.keys()))
        self.assertTrue('000001' in self.archive.book_codes['000000037'])
        self.assertTrue('03_000002' in self.archive.book_codes['000000218'])

    def test_pages(self):
        self.assertEqual(42, len(self.archive.book_codes['000000037']))
