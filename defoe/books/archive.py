"""
Object model representation of ZIP archive of files in
British Library Books-compliant ALTO format.

A ZIP archive corresponds to a document and each file to a page.

The ZIP archive is assumed to hold the following files and
directories:

    <METADATA_CODE>_metadata.xml
    <METADATA_CODE>_metadata.xml
    ...
    ALTO/
        <METADATA_CODE>_<FILE_CODE>.xml
        <METADATA_CODE>_<FILE_CODE>.xml
        ...
        <METADATA_CODE>_<FILE_CODE>.xml
        <METADATA_CODE>_<FILE_CODE>.xml
        ...

where:

* <METADATA_CODE> is [0-9]*
* <FILE_CODE> is [0-9_]*
"""

from defoe.alto.archive import AltoArchive


class Archive(AltoArchive):
    """
    Object model representation of ZIP archive of files in
    British Library Books-compliant ALTO format.
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
        return '([0-9]*)_metadata\.xml'  # pylint: disable=anomalous-backslash-in-string

    def get_page_pattern(self):
        """
        Gets pattern to find filenames corresponding to individual pages.

        :return: pattern
        :rtype: str or unicode
        """
        return 'ALTO\/([0-9]*?)_([0-9_]*)\.xml'  # pylint: disable=anomalous-backslash-in-string

    def get_document_info(self, document_code):
        """
        Gets information from ZIP file about metadata file.

        :param document_code: document file code
        :type document_code: str or unicode
        :return: information
        :rtype: zipfile.ZipInfo
        """
        return self.zip.getinfo(document_code + '_metadata.xml')

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
        return self.zip.getinfo(
            'ALTO/' + document_code + '_' + page_code + '.xml')

    def open_document(self, document_code):
        """
        Opens metadata file.

        :param document_code: document file code
        :type document_code: str or unicode
        :return: stream
        :rtype: zipfile.ZipExt
        """
        return self.zip.open(document_code + '_metadata.xml')

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
        return self.zip.open(
            'ALTO/' + document_code + '_' + page_code + '.xml')
