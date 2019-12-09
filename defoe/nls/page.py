"""
Object model representation of a page represented as an XML file in
METS/MODS format.
"""


from lxml import etree


class Page(object):
    """
    Object model representation of a page represented as an XML file
    in METS/MODS format.
    """
    """ XPath query for Caracther Confidence content """

    def __init__(self, document, code, source=None):
        """
        Constructor.

        :param document: Document object corresponding to document to
        which this page belongs
        :type document: defoe.alto.document.Document
        :param code: identifier for this page within an archive
        :type code: str or unicode
        :param source: stream. If None then an attempt is made to
        open the file holding the page via the given "document"
        :type source: zipfile.ZipExt or another file-like object
        """
        if not source:
            source = document.archive.open_page(document.code, code)
        self.code = code
        self.tree, self.namespaces = self.alto_parse(source)
        self.page_tree = self.alto_page()
        self.width = self.alto_page_width()
        self.height = self.alto_page_height()
        self.pc = self.alto_page_pc()
        self.page_id = self.alto_page_id()
        self.image_nr = self.alto_image_nr()
        self.page_words = None
        self.page_strings = None
        self.page_images = None
        self.page_wc = None
        self.page_cc = None
   


    def alto_parse(self, source):
        xml = etree.parse(source)
        xmlns = xml.getroot().tag.split('}')[0].strip('{')
        return xml, xmlns

    def alto_page(self):
        try:
            return self.tree.find('//{%s}Page' % self.namespaces)
        except:
            return 0 

    def alto_page_width(self):
        try:
            return int(self.page_tree.attrib.get('WIDTH'))
        except:
            return 0

    def alto_page_id(self):
        try:
            return self.page_tree.attrib.get('ID')
        except:
            return '0'
    
    def alto_image_nr(self):
        try:
            return self.page_tree.attrib.get('PHYSICAL_IMG_NR')
        except:
            return '0'

    def alto_page_height(self):
        try:
            return int(self.page_tree.attrib.get('HEIGHT'))
        except:
            return 0 

    def alto_page_pc(self):
        try:
            return self.page_tree.attrib.get('PC')
        except:
            return '0' 

    @property
    def words(self):
        if not self.page_words:
            page_words=[]
            for lines in self.tree.iterfind('.//{%s}TextLine' % self.namespaces):
                for line in lines.findall('{%s}String' % self.namespaces):
                    text = line.attrib.get('CONTENT')
                    page_words.append(text)
            self.page_words = list(map(str,page_words))
        return self.page_words

    @property
    def wc(self):
        if not self.page_wc:
            try:
                for lines in self.tree.iterfind('.//{%s}TextLine' % self.namespaces):
                    for line in lines.findall('{%s}String' % self.namespaces):
                        text = line.attrib.get('WC')
                        self.page_wc.append(text)
            except:
                pass
        return self.page_wc

    @property
    def cc(self):
         if not self.page_cc:
             try:
                 for lines in self.tree.iterfind('.//{%s}TextLine' % self.namespaces):
                     for line in lines.findall('{%s}String' % self.namespaces):
                         text = line.attrib.get('CC')
                         self.page_cc.append(text)
             except:
                 pass
         return self.page_cc

    @property
    def strings(self):
         if not self.page_strings:
             try:
                 for lines in self.tree.iterfind('.//{%s}TextLine' % self.namespaces):
                     for line in lines.findall('{%s}String' % self.namespaces):
                         self.page_strings.append(line)
             except:
                 pass
         return self.page_strings

    @property
    def images(self):
         if not self.page_images:
             try:
                 for graphical in self.tree.iterfind('.//{%s}GraphicalElement' % self.namespaces):
                     graphical_id = graphical.attrib.get('ID')
                     graphical_coords = (graphical.attrib.get('HEIGHT') + ','
                            + graphical.attrib.get('WIDTH') + ','
                            + graphical.attrib.get('VPOS') + ','
                            + graphical.attrib.get('HPOS'))
                     graphical_elements = graphical_id + '=' + graphical_coords
                     self.page_images.append(graphical_elements)
             except:
                 pass
         return self.page_images



    @property
    def content(self):
        """
        Gets all words in page and contatenates together using ' ' as
        delimiter.
        :return: content
        :rtype: str or unicode
        """
        return ' '.join(self.words)
