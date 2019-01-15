"""
Object model representation of ZIP archive of FindMyPast newspapers.
"""

from defoe.alto.archive import AltoArchive


class Archive(AltoArchive):
    """
    Object model representation of ZIP archive of FindMyPast newspapers.
    """

    def __init__(self, filename):
        super(Archive, self).__init__(filename)

    def get_document_pattern(self):
        return '([0-9]*?_[0-9]*?)_mets\.xml'

    def get_page_pattern(self):
        return '([0-9]*?_[0-9]*?)_([0-9_]*)\.xml'

    def zip_info_for_document(self, document_code):
        return self.zip.getinfo(document_code + '_mets.xml')

    def zip_info_for_page(self, document_code, page):
        return self.zip.getinfo(document_code + '_' + page + '.xml')

    def metadata_file(self, document_code):
        return self.zip.open(document_code + '_mets.xml')

    def page_file(self, document_code, page):
        return self.zip.open(document_code + '_' + page + '.xml')
