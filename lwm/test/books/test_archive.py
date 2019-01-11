"""
lwm.books.archive.Archive tests.
"""

from unittest import TestCase

from lwm.books.archive import Archive
from lwm.test.books import fixtures
from lwm.test import open_file


class TestArchive(TestCase):
    """
    lwm.books.archive.Archive tests.
    """

    def setUp(self):
        source = open_file(fixtures,
                           '000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(source)

    def test_books(self):
        self.assertEqual(['000000218', '000000037'],
                         list(self.archive.book_codes.keys()))
        self.assertTrue('000001' in self.archive.book_codes['000000037'])
        self.assertTrue('03_000002' in self.archive.book_codes['000000218'])

    def test_pages(self):
        self.assertEqual(42, len(self.archive.book_codes['000000037']))
