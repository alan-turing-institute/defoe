"""
Object model representation of XML page.
"""

from lxml import etree


class Page(object):
    """
    Object model representation of XML page.
    """

    words_path = etree.XPath('//String/@CONTENT')
    strings_path = etree.XPath('//String')
    images_path = etree.XPath('//GraphicalElement')
    page_path = etree.XPath('//Page')

    def __init__(self, book, code, source=None):
        if not source:
            source = book.archive.page_file(book.code, code)
        self.code = code
        self.tree = etree.parse(source)
        self.page_element = self.single_query(Page.page_path)
        self.width = int(self.page_element.get("WIDTH"))
        self.height = int(self.page_element.get("HEIGHT"))
        self.bwords = None
        self.bstrings = None
        self.bimages = None

    def query(self, query):
        return query(self.tree)

    def single_query(self, query):
        result = self.query(query)
        if not result:
            return None
        return result[0]

    @property
    def words(self):
        if not self.bwords:
            self.bwords = list(map(unicode, self.query(Page.words_path)))
        return self.bwords

    @property
    def strings(self):
        if not self.bstrings:
            self.bstrings = self.query(Page.words_path)
        return self.bstrings

    @property
    def images(self):
        if not self.bimages:
            self.bimages = self.query(Page.images_path)
        return self.bimages

    @property
    def content(self):
        return ' '.join(self.words)

    def reconstruct(self, figure):
        boxen = []
        for element in self.strings:
            boxen.append(
                dict(
                    x=int(element.get('XPOS')),
                    y=int(element.get('YPOS')),
                    width=int(element.get('WIDTH')),
                    height=int(element.get('HEIGHT')),
                    alpha=0.1,
                    content=element.get('CONTENT')
                )
            )
        axes = figure.add_subplot(
            1,
            1,
            1,
            xlim=[0, self.width],
            ylim=[self.height, 0],
            aspect='equal')
        for ebox in boxen:
            ebox['transform'] = axes.transData
            # Render a text patch.
            text = axes.text(ebox.x,
                             ebox.y,
                             ebox.content,
                             verticalalignment='top',
                             horizontalalignment='left')
            # fontsize=font_scaling,bbox=box)
            # Determine bbox in data units.
            renderer = figure.canvas.get_renderer()
            tbox = text.get_window_extent(
                renderer).transformed(axes.transData.inverted())
            # Change fontsize to match true bbox.
            theight = -1.0*tbox.height
            text.set_fontsize(ebox['height']*text.get_fontsize()/theight)
            # Update bbox.
            text.set_bbox(ebox)
