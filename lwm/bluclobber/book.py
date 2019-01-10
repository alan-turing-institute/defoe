"""
Object model representation of XML book.
"""

from collections import defaultdict
import logging
import re

from lxml import etree

from bluclobber.page import Page


class Book(object):
    """
    Object model representation of XML book.
    """

    def __init__(self, code, archive):
        self.namespaces = {
            "mods": 'http://www.loc.gov/mods/v3',
            "mets": 'http://www.loc.gov/METS/'
        }
        self.archive = archive
        self.logger = logging.getLogger('performance')
        self.code = code
        self.pages = None
        self.logger.debug("Loading book metadata")
        self.metadata = self.archive.metadata_file(self.code)
        self.logger.debug("Building book metadata")
        self.tree = etree.parse(self.metadata)
        self.title = self.single_query('//mods:title/text()')
        self.logger.debug("Sorting pages")
        self.page_codes = \
            sorted(self.archive.book_codes[self.code], key=Book.sorter)
        self.pages = len(self.page_codes)
        self.logger.debug("Sorted pages")
        self.years = \
            Book.parse_year(self.single_query('//mods:dateIssued/text()'))
        self.publisher = self.single_query('//mods:publisher/text()')
        self.place = self.single_query('//mods:placeTerm/text()')
        # places often have a year in:
        self.years += Book.parse_year(self.place)
        self.years = sorted(self.years)
        if self.years:
            self.year = self.years[0]
        else:
            self.year = None

    @staticmethod
    def parse_year(text):
        try:
            long_pattern = re.compile("(1[6-9]\d\d)")
            short_pattern = re.compile("\d\d")
            results = []
            chunks = iter(long_pattern.split(text)[1:])
            for year, rest in zip(chunks, chunks):
                results.append(int(year))
                century = year[0:2]
                years = short_pattern.findall(rest)
                for yearxxx in years:
                    results.append(int(century+yearxxx))
            return sorted(set(results))
        except TypeError:
            return []

    @staticmethod
    def sorter(page_code):
        codes = list(map(int, page_code.split('_')))

    def query(self, query):
        return self.tree.xpath(query, namespaces=self.namespaces)

    def page(self, code):
        return Page(self, code)

    def zip_info(self):
        return self.archive.zip_info_for_book(self.code)

    def page_zip_info(self, page_code):
        return self.archive.zip_info_for_page(self.code, page_code)

    def single_query(self, query):
        result = self.query(query)
        if not result:
            return None
        try:
            return str(result[0])
        except UnicodeEncodeError:
            return unicode(result[0])

    def __getitem__(self, index):
        return self.page(self.page_codes[index])

    def __iter__(self):
        for page_code in self.page_codes:
            yield self.page(page_code)

    def strings(self):
        for _, string in self.scan_strings():
            yield string

    def words(self):
        for _, word in self.scan_words():
            yield word

    def images(self):
        for _, image in self.scan_images():
            yield image

    def scan_strings(self):
        for page in self:
            for word in page.strings:
                yield page, word

    def scan_words(self):
        for page in self:
            for word in page.words:
                yield page, word

    def scan_images(self):
        for page in self:
            for image in page.images:
                yield page, image

    def describe_relevant(self, scanner, checker):
        finds = defaultdict(list)
        for target in scanner:
            find = checker(*target)
            if find:
                page, finding = find
                finds[page].append(finding)
        if finds:
            return {self.year:
                    [[self.title, self.year, self.place, self.publisher,
                      [[page.code, page.content, finds]
                       for page, finds in list(finds.items())]]]}
        return None
