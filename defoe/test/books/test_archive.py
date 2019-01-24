"""
defoe.books.archive.Archive tests.
"""

from unittest import TestCase

from defoe.books.archive import Archive
from defoe.file_utils import get_path
from defoe.test.books import fixtures


class TestArchive(TestCase):
    """
    defoe.books.archive.Archive tests.
    """

    def setUp(self):
        self.filename = get_path(
            fixtures,
            '000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(self.filename)

    def test_filename(self):
        self.assertEqual(self.filename, self.archive.filename)

    def test_documents(self):
        self.assertEqual(['000000218', '000000037'],
                         list(self.archive.document_codes.keys()))
        self.assertTrue('000001' in self.archive.document_codes['000000037'])
        self.assertTrue('03_000002' in
                        self.archive.document_codes['000000218'])

    def test_pages(self):
        self.assertEqual(42, len(self.archive.document_codes['000000037']))
