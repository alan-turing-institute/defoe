"""
defoe.papers.issue.Issue tests.
"""

from unittest import TestCase

from defoe.papers.issue import Issue
from defoe.file_utils import get_path
from defoe.test.papers import fixtures


class TestIssue(TestCase):
    """
    defoe.papers.issue.Issue tests.
    """

    def setUp(self):
        """
        Creates Issue from test file fixtures/1912_11_10.xml.
        """
        self.filename = get_path(fixtures, '1912_11_10.xml')
        self.issue = Issue(self.filename)

    def test_filename(self):
        """
        Tests Issue.filename attribute holds expected filename.
        """
        self.assertEqual(self.filename, self.issue.filename)

    def test_newspaper_id(self):
        """
        Tests Issue.newspaper_id attribute holds expected newspaper
        ID.
        """
        self.assertEqual('NID123', self.issue.newspaper_id)

    def test_date(self):
        """
        Tests Issue.date attribute holds expected date.
        """
        self.assertEqual(1912, self.issue.date.year)
        self.assertEqual(11, self.issue.date.month)
        self.assertEqual(10, self.issue.date.day)

    def test_page_count(self):
        """
        Tests Issue.page_count attribute holds expected page count.
        """
        self.assertEqual(1, self.issue.page_count)

    def test_day_of_week(self):
        """
        Tests Issue.day_of_week attribute holds expected day of week.
        """
        self.assertEqual('Monday', self.issue.day_of_week)

    def test_articles_number(self):
        """
        Test Issue.articles holds expected number of issues.
        """
        self.assertEqual(3, len(self.issue.articles))
