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
        """
        Creates Archive from test file
        fixtures/000000037_0_1-42pgs__944211_dat_modified.zip.
        """
        self.filename = get_path(
            fixtures,
            '000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(self.filename)

    def test_filename(self):
        """
        Tests Archive.filename attribute holds expected filename.
        """
        self.assertEqual(self.filename, self.archive.filename)

    def test_document_codes(self):
        """
        Tests Document.document_codes attribute holds the expected document
        codes.
        """
        codes = list(self.archive.document_codes.keys())
        self.assertEqual(2, len(codes))
        for code in ['000000218', '000000037']:
            self.assertTrue(code in codes)

    def test_document_codes_pages(self):
        """
        Tests Document.document_codes attribute holds the expected
        number of pages and expected page codes for each document.
        """
        codes = self.archive.document_codes
        self.assertEqual(42, len(codes['000000037']))
        self.assertTrue('000001' in codes['000000037'])
        self.assertEqual(306, len(codes['000000218']))
        self.assertTrue('03_000002' in codes['000000218'])
