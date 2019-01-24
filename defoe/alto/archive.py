"""
Abstract base class for object model representation of ZIP archive
of files in ALTO format.
"""

import abc
import re
import zipfile

from defoe.alto.document import Document
from defoe.spark_utils import open_stream


class AltoArchive(object):
    """
    Abstract base class for object model representation of ZIP archive
    of files in ALTO format.
    """
    __metaclass__ = abc.ABCMeta

    """
    Constructor

    :param filename: archive filename
    :type: filename: str or unicode
    """
    def __init__(self, filename):
        self.filename = filename
        stream = open_stream(self.filename)
        self.zip = zipfile.ZipFile(stream)
        self.filenames = [entry.filename for entry in self.zip.infolist()]
        document_pattern = re.compile(self.get_document_pattern())
        page_pattern = re.compile(self.get_page_pattern())
        document_matches = [
            _f for _f in [document_pattern.match(name) for name in self.filenames] if _f]
        page_matches = [
            _f for _f in [page_pattern.match(name) for name in self.filenames] if _f]
        self.document_codes = {match.group(1): [] for match in document_matches}
        for match in page_matches:
            self.document_codes[match.group(1)].append(match.group(2))

    def __getitem__(self, index):
        return Document(list(self.document_codes.keys())[index], self)

    def __iter__(self):
        for document in self.document_codes:
            yield Document(document, self)

    def __len__(self):
        return len(self.document_codes)

    """
    Gets pattern to find metadata filename which has information about
    the document as a whole.

    :return: pattern
    :rtype: str or unicode
    """
    @abc.abstractmethod
    def get_document_pattern(self):
        return

    """
    Gets pattern to find filenames corresponding to individual pages.

    :return: pattern
    :rtype: str or unicode
    """
    @abc.abstractmethod
    def get_page_pattern(self):
        return

    """
    Gets information from ZIP file about metadata file.

    :param document_code: document file code
    :type document_code: str or unicode
    :return: information
    :rtype: zipfile.ZipInfo
    """
    @abc.abstractmethod
    def get_document_info(self, document_code):
        return

    """
    Gets information from ZIP file about a page file.

    :param document_code: page file code
    :type document_code: str or unicode
    :param page_code: file code
    :type page_code: str or unicode
    :return: information
    :rtype: zipfile.ZipInfo
    """
    @abc.abstractmethod
    def get_page_info(self, document_code, page_code):
        return

    """
    Opens metadata file.

    :param document_code: document file code
    :type document_code: str or unicode
    :return: stream
    :rtype: zipfile.ZipExt
    """
    @abc.abstractmethod
    def open_document(self, document_code):
        return

    """
    Opens page file.

    :param document_code: page file code
    :type document_code: str or unicode
    :param page_code: file code
    :type page_code: str or unicode
    :return: stream
    :rtype: zipfile.ZipExt
    """
    @abc.abstractmethod
    def open_page(self, document_code, page_code):
        return
