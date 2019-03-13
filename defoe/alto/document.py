"""
Object model representation of a document represented as a collection
of XML files in METS/MODS format.
"""
import re

from lxml import etree

from defoe.alto.page import Page


class Document(object):
    """
    Object model representation of a document represented as a
    collection of XML files in METS/MODS format.
    """

    def __init__(self, code, archive):
        """
        Constructor

        :param code: identifier for this document within an archive
        :type code: str or unicode
        :param archive: archive to which this document belongs
        :type archive: defoe.alto.archive.Archive
        """
        self.namespaces = {
            "mods": 'http://www.loc.gov/mods/v3',
            "mets": 'http://www.loc.gov/METS/'
        }
        self.archive = archive
        self.code = code
        self.num_pages = 0
        self.metadata = self.archive.open_document(self.code)
        self.metadata_tree = etree.parse(self.metadata)
        self.title = self.single_query('//mods:title/text()')
        self.page_codes = \
            sorted(self.archive.document_codes[self.code], key=Document.sorter)
        self.num_pages = len(self.page_codes)
        self.years = \
            Document.parse_year(self.single_query('//mods:dateIssued/text()'))
        self.publisher = self.single_query('//mods:publisher/text()')
        self.place = self.single_query('//mods:placeTerm/text()')
        # place may often have a year in.
        self.years += Document.parse_year(self.place)
        self.years = sorted(self.years)
        if self.years:
            self.year = self.years[0]
        else:
            self.year = None

    @staticmethod
    def parse_year(text):
        """
        Parse text to extract years of form 16xx to 19xx.

        Any date of form NN following a year of form CCYY to CCYY
        is used to derive a date CCNN.

        As an exception to this rule, single years are parsed
        from dates precisely matching the format YYYY-MM-DD.

        For example:

        * "1862, [1861]" returns [1861, 1862]
        * "1847 [1846, 47]" returns [1846, 1847]
        * "1873-80" returns [1873, 1880]
        * "1870-09-01" returns [1870]

        :param text: text to parse
        :type text: str or unicode
        :return: years
        :rtype: set(int)
        """
        try:
            date_pattern = re.compile("(1[6-9]\d{2}(-|/)(0[1-9]|1[0-2])(-|/)(0[1-9]|[12]\d|3[01]))")
            if date_pattern.match(text):
                return [int(text[0:4])]
            long_pattern = re.compile("(1[6-9]\d\d)")
            short_pattern = re.compile("\d\d")
            results = []
            chunks = iter(long_pattern.split(text)[1:])
            for year, rest in zip(chunks, chunks):
                results.append(int(year))
                century = year[0:2]
                short_years = short_pattern.findall(rest)
                for short_year in short_years:
                    results.append(int(century + short_year))
            return sorted(set(results))
        except TypeError:
            return []

    @staticmethod
    def sorter(page_code):
        """
        Given a page code of form [0-9]*(_[0-9]*), split this
        into the sub-codes. For example, given 123_456, return
        [123, 456]

        :param page_code: page code
        :type page_code: str or unicode
        :return: list of page codes
        :rtype: list(int)
        """
        codes = list(map(int, page_code.split('_')))
        return codes

    def query(self, query):
        """
        Run XPath query.

        :param query: XPath query
        :type query: str or unicode
        :return: list of query results or None if none
        :rtype: list(lxml.etree.<MODULE>) (depends on query)
        """
        return self.metadata_tree.xpath(query, namespaces=self.namespaces)

    def single_query(self, query):
        """
        Run XPath query and return first result.

        :param query: XPath query
        :type query: str or unicode
        :return: query result or None if none
        :rtype: str or unicode
        """
        result = self.query(query)
        if not result:
            return None
        try:
            return str(result[0])
        except UnicodeEncodeError:
            return unicode(result[0])

    def page(self, code):
        """
        Given a page code, return a new Page object.

        :param code: page code
        :type code: str or unicode
        :return: Page object
        :rtype: defoe.alto.page.Page
        """
        return Page(self, code)

    def get_document_info(self):
        """
        Gets information from ZIP file about metadata file
        corresponding to this document.

        :return: information
        :rtype: zipfile.ZipInfo
        """
        return self.archive.get_document_info(self.code)

    def get_page_info(self, page_code):
        """
        Gets information from ZIP file about a page file within
        this document.

        :param page_code: file code
        :type page_code: str or unicode
        :return: information
        :rtype: zipfile.ZipInfo
        """
        return self.archive.get_page_info(self.code, page_code)

    def __getitem__(self, index):
        """
        Given a page index, return a new Page object.

        :param index: page index
        :type index: int
        :return: Page object
        :rtype: defoe.alto.page.Page
        """
        return self.page(self.page_codes[index])

    def __iter__(self):
        """
        Iterate over page codes, returning new Page objects.

        :return: Page object
        :rtype: defoe.alto.page.Page
        """
        for page_code in self.page_codes:
            yield self.page(page_code)

    def scan_strings(self):
        """
        Iterate over strings in pages.

        :return: page and string
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for string in page.strings:
                yield page, string

    def scan_words(self):
        """
        Iterate over words in pages.

        :return: page and word
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for word in page.words:
                yield page, word

    def scan_images(self):
        """
        Iterate over images in pages.

        :return: page and XML fragment with image
        :rtype: tuple(defoe.alto.page.Page, lxml.etree._Element)
        """
        for page in self:
            for image in page.images:
                yield page, image

    def strings(self):
        """
        Iterate over strings.

        :return: string
        :rtype: str or unicode
        """
        for _, string in self.scan_strings():
            yield string

    def words(self):
        """
        Iterate over strings.

        :return: word
        :rtype: str or unicode
        """
        for _, word in self.scan_words():
            yield word

    def images(self):
        """
        Iterate over images.

        :return: XML fragment with image
        :rtype: lxml.etree._Element
        """
        for _, image in self.scan_images():
            yield image
