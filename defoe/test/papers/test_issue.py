"""
defoe.papers.issue.Issue tests.
"""

from unittest import TestCase

from defoe.papers.issue import Issue
from defoe.test.papers import fixtures
from defoe.test import get_path


class TestIssue(TestCase):
    """
    defoe.papers.issue.Issue tests.
    """

    def setUp(self):
        """
        Load the standard test file
        """
        self.filename = get_path(fixtures, '1912_11_10.xml')
        self.issue = Issue(self.filename)

    def test_filename(self):
        """
        Test that the filename is correct
        """
        self.assertEqual(self.filename, self.issue.filename)

    def test_newspaper_id(self):
        """
        Test that the newspaper ID is correct
        """
        self.assertEqual('NID123', self.issue.newspaper_id)

    def test_date(self):
        """
        Test that the date is correct
        """
        self.assertEqual(1912, self.issue.date.year)
        self.assertEqual(11, self.issue.date.month)
        self.assertEqual(10, self.issue.date.day)

    def test_page_count(self):
        """
        Test that the page count is correct.
        """
        self.assertEqual(1, self.issue.page_count)

    def test_day_of_week(self):
        """
        Test that the day of the week is correct.
        """
        self.assertEqual('Monday', self.issue.day_of_week)

    def test_articles_per_issue(self):
        """
        Test that the articles per issue is correct.
        """
        self.assertEqual(3, len(self.issue.articles))
