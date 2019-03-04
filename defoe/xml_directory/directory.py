"""
Object model representation of an XML document directory.
"""

import os
import os.path
from lxml import etree


class Directory(object):
    """
    Object model representation of an XML document directory.
    """

    def __init__(self, directory):
        """
        Constructor.

        :param directory: XML directory
        :type: directory: str or unicode
        """
        self.directory = directory
        self.files = os.listdir(directory)
        self.mets = []
        self.prefixes = set()
        for f in self.files:
            if f.lower().endswith("_mets.xml"):
                self.mets.append(f)
            splitter = f.rfind("_")
            if splitter > -1:
                self.prefixes.add(f[0:splitter])
