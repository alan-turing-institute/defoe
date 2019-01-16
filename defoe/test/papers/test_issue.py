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
        self.filename = get_path(fixtures, '2000_04_24.xml')
        self.issue = Issue(self.filename)

    def test_filename(self):
        """
        Test that the filename is correct
        """
        self.assertEqual(self.filename, self.issue.filename)

    def test_date(self):
        """
        Test that the date is correct
        """
        self.assertEqual(2000, self.issue.date.year)
        self.assertEqual(4, self.issue.date.month)
        self.assertEqual(24, self.issue.date.day)

    def test_page_count(self):
        """
        Test that the page count is correct.
        """
        self.assertEqual(88, self.issue.page_count)

    def test_day_of_week(self):
        """
        Test that the day of the week is correct.
        """
        self.assertEqual('Monday', self.issue.day_of_week)

    def test_articles_per_issue(self):
        """
        Test that the articles per issue is correct.
        """
        self.assertEqual(580, len(self.issue.articles))
