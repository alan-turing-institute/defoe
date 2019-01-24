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

    """
    Constructor

    :param filename: archive filename
    :type: filename: str or unicode
    """
    def __init__(self, filename):
        AltoArchive.__init__(self, filename)

    """
    Gets pattern to find metadata filename which has information about
    the document as a whole.

    :return: pattern
    :rtype: str or unicode
    """
    def get_document_pattern(self):
        return '([0-9]*)_metadata\.xml'

    """
    Gets pattern to find filenames corresponding to individual pages.

    :return: pattern
    :rtype: str or unicode
    """
    def get_page_pattern(self):
        return 'ALTO\/([0-9]*?)_([0-9_]*)\.xml'

    """
    Gets information from ZIP file about metadata file.

    :param document_code: document file code
    :type document_code: str or unicode
    :return: information
    :rtype: zipfile.ZipInfo
    """
    def get_document_info(self, document_code):
        return self.zip.getinfo(document_code + '_metadata.xml')

    """
    Gets information from ZIP file about a page file.

    :param document_code: page file code
    :type document_code: str or unicode
    :param page_code: file code
    :type page_code: str or unicode
    :return: information
    :rtype: zipfile.ZipInfo
    """
    def get_page_info(self, document_code, page_code):
        return self.zip.getinfo(
            'ALTO/' + document_code + '_' + page_code + '.xml')

    """
    Opens metadata file.

    :param document_code: document file code
    :type document_code: str or unicode
    :return: stream
    :rtype: zipfile.ZipExt
    """
    def open_document(self, document_code):
        return self.zip.open(document_code + '_metadata.xml')

    """
    Opens page file.

    :param document_code: page file code
    :type document_code: str or unicode
    :param page_code: file code
    :type page_code: str or unicode
    :return: stream
    :rtype: zipfile.ZipExt
    """
    def open_page(self, document_code, page_code):
        return self.zip.open(
            'ALTO/' + document_code + '_' + page_code + '.xml')
