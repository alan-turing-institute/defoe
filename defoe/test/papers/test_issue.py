"""
defoe.papers.issue.Issue tests.
"""

from unittest import TestCase


class TestIssue(TestCase):
    """
    defoe.papers.issue.Issue tests.
    """

    __test__ = False

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
        self.assertEqual(self.issue_id, self.issue.newspaper_id)

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

    def test_articles_number(self):
        """
        Test Issue.articles holds expected number of issues.
        """
        self.assertEqual(3, len(self.issue.articles))
