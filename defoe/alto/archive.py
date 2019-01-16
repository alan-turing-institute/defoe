"""
Abstract base class for object model representation of ZIP archive
of ALTO documents.
"""

import abc
from cStringIO import StringIO
import logging
import re
import zipfile

from defoe.alto.document import Document
from defoe.file_utils import open_stream


class AltoArchive(object):
    """
    Abstract base class for object model representation of ZIP archive
    of ALTO documents.
    """
    __metaclass__=abc.ABCMeta

    def __init__(self, filename):
        self.logger = logging.getLogger('performance')
        self.logger.info("Opening archive")
        self.filename = filename
        stream = open_stream(self.filename)
        self.logger.debug("Opened archive")
        self.zip = zipfile.ZipFile(stream)
        self.logger.info("Slurped archive")
        self.logger.debug("Examining documents in archive")
        self.filenames = [entry.filename for entry in self.zip.infolist()]
        self.logger.debug("Enumerating documents")
        document_pattern = re.compile(self.get_document_pattern())
        page_pattern = re.compile(self.get_page_pattern())
        document_matches = [
            _f for _f in [document_pattern.match(name) for name in self.filenames] if _f]
        page_matches = [
            _f for _f in [page_pattern.match(name) for name in self.filenames] if _f]
        self.document_codes = {match.group(1): [] for match in document_matches}
        for match in page_matches:
            self.document_codes[match.group(1)].append(match.group(2))
        self.logger.info("Enumerated documents")

    @abc.abstractmethod
    def get_document_pattern(self):
        return

    @abc.abstractmethod
    def get_page_pattern(self):
        return

    @abc.abstractmethod
    def zip_info_for_document(self, document_code):
        return

    @abc.abstractmethod
    def zip_info_for_page(self, document_code, page):
        return

    @abc.abstractmethod
    def metadata_file(self, document_code):
        return

    @abc.abstractmethod
    def page_file(self, document_code, page):
        return

    def __getitem__(self, index):
        self.logger.debug("Creating document")
        return Document(list(self.document_codes.keys())[index], self)

    def __iter__(self):
        for document in self.document_codes:
            self.logger.debug("Creating document")
            yield Document(document, self)

    def __len__(self):
        return len(self.document_codes)
