"""
Object model representation of ZIP archive of files in
Find My Past Newspapers-compliant ALTO format.

A ZIP archive corresponds to a document and each file to a page.

The ZIP archive is assumed to hold the following files:

    <METADATA_CODE>_mets.xml
    <METADATA_CODE>_<FILE_CODE>.xml
    <METADATA_CODE>_<FILE_CODE>.xml
    ...
    <METADATA_CODE>_mets.xml
    <METADATA_CODE>_<FILE_CODE>.xml
    <METADATA_CODE>_<FILE_CODE>.xml
    ...

where:

* <METADATA_CODE> is [0-9]*?_[0-9]*?
* <FILE_CODE> is [0-9_]*
"""

from defoe.fmp.archive_combine import AltoArchive
from defoe.spark_utils import open_stream


class Archive(AltoArchive):
    """
    Object model representation of archive of files in
    Find My Past Newspapers-compliant ALTO format.
    """

    def __init__(self, filename):
        """
        Constructor

        :param filename: archive filename
        :type: filename: str or unicode
        """
        AltoArchive.__init__(self, filename)

    def get_document_pattern(self):
        """
        Gets pattern to find metadata filename which has information about
        the document as a whole.

        :return: pattern
        :rtype: str or unicode
        """
        return '([0-9]*?_[0-9]*?)_mets\.xml'  # pylint: disable=anomalous-backslash-in-string

    def get_page_pattern(self):
        """
        Gets pattern to find filenames corresponding to individual pages.

        :return: pattern
        :rtype: str or unicode
        """
        return '([0-9]*?_[0-9]*?)_([0-9_]*)\.xml'  # pylint: disable=anomalous-backslash-in-string

    def get_document_info(self, document_code):
        """
        Gets information from ZIP file about metadata file.

        :param document_code: document file code
        :type document_code: str or unicode
        :return: information
        :rtype: zipfile.ZipInfo
        """
        if ".zip" in self.filename:
            return self.zip.getinfo(document_code + '_mets.xml')
        else:
            return

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
        if ".zip" in self.filename:
            return self.zip.getinfo(document_code + '_' + page_code + '.xml')
        else:
            return

    def open_document(self, document_code):
        """
        Opens metadata file.

        :param document_code: document file code
        :type document_code: str or unicode
        :return: stream
        """
        if ".zip" in self.filename:
            return self.zip.open(document_code + '_mets.xml')
        else:
            return open_stream(self.filename+"/"+document_code + '_mets.xml')

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
        if ".zip" in self.filename:
            return self.zip.open(document_code + '_' + page_code + '.xml')
        else:
            return open_stream(self.filename+"/"+document_code + '_' + page_code + '.xml')
