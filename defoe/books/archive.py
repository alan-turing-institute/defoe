"""
Object model representation of ZIP archive of books.
"""

from defoe.alto.archive import AltoArchive


class Archive(AltoArchive):
    """
    Object model representation of ZIP archive of books.
    """

    def __init__(self, filename):
        super(Archive, self).__init__(filename)

    def get_document_pattern(self):
        return '([0-9]*)_metadata\.xml'

    def get_page_pattern(self):
        return 'ALTO\/([0-9]*?)_([0-9_]*)\.xml'

    def zip_info_for_document(self, document_code):
        return self.zip.getinfo(document_code + '_metadata.xml')

    def zip_info_for_page(self, document_code, page):
        return self.zip.getinfo('ALTO/' + document_code + '_' + page + '.xml')

    def metadata_file(self, document_code):
        return self.zip.open(document_code + '_metadata.xml')

    def page_file(self, document_code, page):
        return self.zip.open('ALTO/' + document_code + '_' + page + '.xml')
