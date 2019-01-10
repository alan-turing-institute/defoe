"""
Object model representation of ZIP archive of books.
"""

from cStringIO import StringIO
import logging
import re
import zipfile

from bluclobber.book import Book


class Archive(object):
    """
    Object model representation of ZIP archive of books.
    """

    def __init__(self, stream):
        self.logger = logging.getLogger('performance')
        self.logger.info("Opening archive")
        mmap = StringIO(stream.read())
        self.logger.debug("Opened archive")
        self.zip = zipfile.ZipFile(mmap)
        self.logger.info("Slurped archive")
        self.logger.debug("Examining books in archive")
        self.filenames = [entry.filename for entry in self.zip.infolist()]
        self.logger.debug("Enumerating books")
        book_pattern = re.compile('([0-9]*)_metadata\.xml')
        page_pattern = re.compile('ALTO\/([0-9]*?)_([0-9_]*)\.xml')
        book_matches = [
            _f for _f in [book_pattern.match(name) for name in self.filenames] if _f]
        page_matches = [
            _f for _f in [page_pattern.match(name) for name in self.filenames] if _f]
        self.book_codes = {match.group(1): [] for match in book_matches}
        for match in page_matches:
            self.book_codes[match.group(1)].append(match.group(2))
        self.logger.info("Enumerated books")

    def zip_info_for_book(self, book_code):
        return self.zip.getinfo(book_code + '_metadata.xml')

    def zip_info_for_page(self, book_code, page):
        return self.zip.getinfo('ALTO/' + book_code + '_' + page + '.xml')

    def metadata_file(self, book_code):
        return self.zip.open(book_code + '_metadata.xml')

    def page_file(self, book_code, page):
        return self.zip.open('ALTO/' + book_code + '_' + page + '.xml')

    def __getitem__(self, index):
        self.logger.debug("Creating book")
        return Book(list(self.book_codes.keys())[index], self)

    def __iter__(self):
        for book in self.book_codes:
            self.logger.debug("Creating book")
            yield Book(book, self)

    def __len__(self):
        return len(self.book_codes)
