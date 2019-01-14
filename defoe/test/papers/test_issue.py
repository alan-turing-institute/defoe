"""
defoe.papers.issue.Issue tests.
"""

from unittest import TestCase

from defoe.papers.issue import Issue
from defoe.test.papers import fixtures
from defoe.test import open_file


class TestIssue(TestCase):
    """
    defoe.papers.issue.Issue tests.
    """

    def setUp(self):
        """
        Load the standard test file
        """
        source = open_file(fixtures, '2000_04_24.xml')
        self.issue = Issue(source)

    def test_date(self):
        """
        Test that the date is correct
        """
        assert self.issue.date.year == 2000
        assert self.issue.date.month == 4
        assert self.issue.date.day == 24

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
