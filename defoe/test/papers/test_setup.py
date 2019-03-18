"""
defoe.papers.setup tests.
"""

from unittest import TestCase

from defoe.papers.issue import Issue
from defoe.papers.setup import filename_to_object
from defoe.file_utils import get_path
from defoe.test.papers import fixtures


class TestSetup(TestCase):
    """
    defoe.papers.setup tests.
    """

    def test_filename_to_object(self):
        """
        Tests filename_to_object with valid XML file results in a
        tuple with an Issue.
        """
        filename = get_path(fixtures, '1912_11_10_bl.xml')
        result = filename_to_object(filename)
        self.assertTrue(result[0] is not None)
        self.assertTrue(isinstance(result[0], Issue))
        self.assertEqual(None, result[1])

    def test_filename_to_object_bad_xml(self):
        """
        Tests filename_to_object with a bad XML file results in a
        tuple with a filename and an error message.
        """
        filename = get_path(fixtures, 'bad.xml')
        result = filename_to_object(filename)
        self.assertTrue(result[0] is not None)
        self.assertTrue(isinstance(result[0], str))
        self.assertEqual(filename, result[0])
        self.assertTrue(result[1] is not None)
        self.assertTrue(isinstance(result[1], str))
        self.assertTrue("Missing 'issue' element" in str(result[1]))

    def test_filename_to_object_no_such_file(self):
        """
        Tests filename_to_object with a non-existant file results in a
        tuple with a filename and an error message.
        """
        filename = get_path(fixtures, 'no-such-file.xml')
        result = filename_to_object(filename)
        self.assertTrue(result[0] is not None)
        self.assertTrue(isinstance(result[0], str))
        self.assertEqual(filename, result[0])
        self.assertTrue(result[1] is not None)
        self.assertTrue(isinstance(result[1], str))
        self.assertTrue("No such file or directory" in str(result[1]))
