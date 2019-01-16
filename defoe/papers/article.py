"""
Object model representation of XML Article.


Module for articles, many of which make up an issue
"""

from logging import getLogger


class Article(object):
    """
    Class to represent an article in an issue of an newspaper
    """
    def __init__(self, source, filename):
        """
        Create the article from source XML
        """
        self.logger = getLogger('py4j')
        self.tree = source
        self.filename = filename
        # DTD says only one text element per article
        # Texts can have different children: preamble, title and cr. Each of
        # those is formed by pg (position guide) and p (paragraph) elements.
        # Paras are  made of words (wd).
        self.quality = self.tree.xpath('ocr/text()')
        if not self.quality:
            self.quality = None
        elif len(self.quality) == 1:
            self.quality = float(self.quality[0])
        else:
            self.logger.info('Multiple OCR qualities found. Dropping.')
            self.quality = None
        self.title = self.tree.xpath('text/text.title/p/wd/text()')
        self.preamble = self.tree.xpath('text/text.preamble/p/wd/text()')
        self.content = self.tree.xpath('text/text.cr/p/wd/text()')

#        page_total = tree.xpath('pi/text()')    
#        page = []
#        for i in page_total:
#            page.append(i.split("_")[-1]) # [0001, 0002, 0003,...]
#        # Split on "_" OR "-"
#        self.pages = " ".join(page).replace(' - ', '') # '0001, 0002, 0003,...#'
#        self.xml_id = page_total[0].split("_")[:2] # [0000164, 19070603]
#        self.issue_id = "_".join(xml_id) # '0000164_19070603'
#        self.newspaper_id = page_total[0].split("_")[:1] # [0000164]
#        self.newspaper_id = "".join(self_newspaper_id) # 0000164

    @property
    def words(self):
        """
        Get the full text of the article, title etc.abs as a list of tokens
        """
        return self.title + self.preamble + self.content

    @property
    def words_string(self):
        """
        Return the full text of the article as a string. Remove all hyphens.
        This merges hyphenated word by may cause problems with subordinate
        clauses (The sheep - the really loud one - had just entered my office).
        """
        return ' '.join(self.words).replace(' - ', '')
