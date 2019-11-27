"""
Abstract base class for object model representation of [ZIP] archive
of files in ALTO format.
"""

import abc
import re
import zipfile

from defoe.nls.document import Document
from defoe.spark_utils import open_stream
from os import listdir
from os.path import isfile, join


class AltoArchive(object, metaclass=abc.ABCMeta):
    """
    Abstract base class for object model representation of [ZIP] archive
    of files in ALTO format.
    """

    def __init__(self, filename):
        """
        Constructor

        :param filename: archive filename
        :type: filename: str or unicode
        """
        self.filename = filename
        if ".zip" in self.filename:
            stream = open_stream(self.filename)
            self.zip = zipfile.ZipFile(stream)
            self.filenames = [entry.filename for entry in self.zip.infolist()]
        else:
             self.filenames= []
             for entry in listdir(self.filename):
                  if not isfile(join(self.filename, entry)):
                      for i in listdir(join(self.filename,entry)):
                          self.filenames.append(entry+"/"+i)
                  else:
                      self.filenames.append(entry)
        document_pattern = re.compile(self.get_document_pattern())
        page_pattern = re.compile(self.get_page_pattern())
        document_matches = [
            _f for _f in [document_pattern.match(name) for name in self.filenames] if _f]
        page_matches = [
            _f for _f in [page_pattern.match(name) for name in self.filenames] if _f]
        self.document_codes = {match.group(1): [] for match in document_matches}
        document_name=list(self.document_codes.keys())[0]
        for match in page_matches:
            self.document_codes[document_name].append(match.group(0))

    def __getitem__(self, index):
        """
        Given a document index, return a new Document object.

        :param index: document index
        :type index: int
        :return: Document object
        :rtype: defoe.alto.document.Document
        """
        return Document(list(self.document_codes.keys())[index], self)

    def __iter__(self):
        """
        Iterate over document codes, creating Document objects.

        :return: Document object
        :rtype: defoe.alto.document.Document
        """
        for document in self.document_codes:
            yield Document(document, self)

    def __len__(self):
        """
        Gets number of documents in [ZIP] archive.

        :return: number of documents
        :rtype: int
        """
        return len(self.document_codes)

    @abc.abstractmethod
    def get_document_pattern(self):
        """
        Gets pattern to find metadata filename which has information about
        the document as a whole.

        :return: pattern
        :rtype: str or unicode
        """
        return

    @abc.abstractmethod
    def get_page_pattern(self):
        """
        Gets pattern to find filenames corresponding to individual pages.

        :return: pattern
        :rtype: str or unicode
        """
        return

    @abc.abstractmethod
    def get_document_info(self, document_code):
        """
        Gets information from ZIP file about metadata file.

        :param document_code: document file code
        :type document_code: str or unicode
        :return: information
        :rtype: zipfile.ZipInfo
        """
        return

    @abc.abstractmethod
    def get_page_info(self, document_code, page_code):
        """
        Gets information from ZIP file about a page file.

        :param document_code: page file code
        :type document_code: str or unicode
        :param page_code: file code
        :type page_code: str or unicode
        :return: information
        :rtype: zipfile.ZipInfo
        """
        return

    @abc.abstractmethod
    def open_document(self, document_code):
        """
        Opens metadata file.

        :param document_code: document file code
        :type document_code: str or unicode
        :return: stream
        :rtype: zipfile.ZipExt
        """
        return

    @abc.abstractmethod
    def open_page(self, document_code, page_code):
        """
        Opens page file.

        :param document_code: page file code
        :type document_code: str or unicode
        :param page_code: file code
        :type page_code: str or unicode
        :return: stream
        :rtype: zipfile.ZipExt
        """
        return
