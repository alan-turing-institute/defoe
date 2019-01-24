"""
defoe.alto.document.Document (via defoe.books.archive.Archive) tests.
"""

from unittest import TestCase

from defoe.books.archive import Archive
from defoe.file_utils import get_path
from defoe.test.books import fixtures


class TestDocument(TestCase):
    """
    defoe.alto.document.Document (via defoe.books.archive.Archive)
    tests.
    """

    def setUp(self):
        """
        Creates Archive from test file
        fixtures/000000037_0_1-42pgs__944211_dat_modified.zip then
        retrieves first Document.
        """
        source = get_path(fixtures,
                          '000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(source)
        self.document = self.archive[0]

    def test_title(self):
        """
        Tests Document.title attribute holds the expected title.
        """
        self.assertTrue("Love the Avenger" in self.document.title)

    def test_place(self):
        """
        Tests Document.place attribute holds the expected number of
        places and includes an expected place.
        """
        place = self.document.place
        self.assertEqual(13, len(place))
        self.assertTrue("London" in place)

    def test_code(self):
        """
        Tests Document.code attribute the holds expected document
        code, that the document code is in the archive's record of
        documents, and that an expected page code is in the
        archive's record of pages.
        """
        self.assertEqual('000000218', self.document.code)
        self.assertTrue(self.document.code in self.archive.document_codes)
        self.assertTrue('03_000002' in
                        self.archive.document_codes[self.document.code])

    def test_page_codes(self):
        """
        Tests Document.page_codes attribute holds the expected number
        of page codes and includes an expected page code.
        """
        page_codes = self.document.page_codes
        self.assertEqual(306, len(page_codes))
        self.assertTrue('03_000002' in page_codes)

    def test_num_pages(self):
        """
        Tests Document.num_pages property holds the expected number of
        pages.
        """
        self.assertEqual(306, self.document.num_pages)

    def test_page_content(self):
        """
        Tests Document holds a page which includes an expected
        phrase.
        """
        self.assertTrue(("the great Avorld of Paris" in
                         self.document[25].content))
