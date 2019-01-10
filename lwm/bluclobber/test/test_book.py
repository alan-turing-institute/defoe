"""
bluclobber.book.Book tests.
"""

from unittest import TestCase

from bluclobber.archive import Archive
from bluclobber.book import Book
from bluclobber.test.fixtures import open_file


class TestBook(TestCase):
    """
    bluclobber.book.Book tests.
    """

    def setUp(self):
        source = open_file('000000037_0_1-42pgs__944211_dat_modified.zip')
        self.archive = Archive(source)
        self.book = self.archive[0]

    def test_title(self):
        self.assertTrue("Love the Avenger" in self.book.title)

    def test_place(self):
        self.assertTrue("London" in self.book.place)

    def test_code(self):
        self.assertEqual('000000218', self.book.code)
        self.assertTrue(self.book.code in self.archive.book_codes)
        self.assertTrue('03_000002' in
                        self.archive.book_codes[self.book.code])

    def test_page_codes(self):
        self.assertTrue('03_000002' in self.book.page_codes)

    def test_pages(self):
        self.assertEqual(306, self.book.pages)

    def test_content(self):
        self.assertTrue(("the great Avorld of Paris" in
                         self.book[25].content))

    def test_year(self):
        self.assertEqual([1823, 1869], self.book.years)

    def test_yearify(self):
        fixtures = {
            "[1866]": [1866],
            "1885]": [1885],
            "1847 [1846, 47]": [1846, 1847],
            "1862, [1861]": [1861, 1862],
            "1873-80": [1873, 1880],
            "[ca. 1730]": [1730],
            "1725, 26": [1725, 1726],
        }
        for case, expected in list(fixtures.items()):
            self.assertEqual(expected, Book.parse_year(case))
