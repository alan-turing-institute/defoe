"""
defoe.papers.issue.Issue tests for newspapers conforming to
nccoissue.dtd.
"""

from defoe.papers.issue import Issue
from defoe.file_utils import get_path
from defoe.test.papers import fixtures
from defoe.test.papers.test_issue import TestIssue


class TestIssueNcco(TestIssue):
    """
    defoe.papers.issue.Issue tests for newspapers conforming to
    nccoissue.dtd.
    """

    __test__ = True

    def setUp(self):
        """
        Creates Issue from test file fixtures/1912_11_10_ncco.xml.
        """
        self.filename = get_path(fixtures, '1912_11_10_ncco.xml')
        self.issue = Issue(self.filename)
        self.issue_id = "NID123-1912-NOV10"
