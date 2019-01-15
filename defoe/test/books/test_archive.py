"""
defoe.books.archive.Archive tests.
"""

from unittest import TestCase

from defoe.books.archive import Archive
from defoe.test.books import fixtures
from defoe.test import get_path


class TestArchive(TestCase):
    """
    defoe.books.archive.Archive tests.
    """

    def setUp(self):
        source = get_path(fixtures,
                          '000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(source)

    def test_documents(self):
        self.assertEqual(['000000218', '000000037'],
                         list(self.archive.document_codes.keys()))
        self.assertTrue('000001' in self.archive.document_codes['000000037'])
        self.assertTrue('03_000002' in
                        self.archive.document_codes['000000218'])

    def test_pages(self):
        self.assertEqual(42, len(self.archive.document_codes['000000037']))
