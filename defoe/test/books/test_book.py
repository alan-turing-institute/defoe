"""
defoe.books.book.Book tests.
"""

from unittest import TestCase

from defoe.books.archive import Archive
from defoe.file_utils import get_path
from defoe.test.books import fixtures


class TestBook(TestCase):
    """
    defoe.books.book.Book tests.
    """

    def setUp(self):
        source = get_path(fixtures,
                          '000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(source)
        self.book = self.archive[0]

    def test_title(self):
        self.assertTrue("Love the Avenger" in self.book.title)

    def test_place(self):
        self.assertTrue("London" in self.book.place)

    def test_code(self):
        self.assertEqual('000000218', self.book.code)
        self.assertTrue(self.book.code in self.archive.document_codes)
        self.assertTrue('03_000002' in
                        self.archive.document_codes[self.book.code])

    def test_page_codes(self):
        self.assertTrue('03_000002' in self.book.page_codes)

    def test_pages(self):
        self.assertEqual(306, self.book.num_pages)

    def test_content(self):
        self.assertTrue(("the great Avorld of Paris" in
                         self.book[25].content))

    def test_year(self):
        self.assertEqual([1823, 1869], self.book.years)
