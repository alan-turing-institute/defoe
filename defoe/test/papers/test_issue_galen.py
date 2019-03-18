"""
defoe.papers.issue.Issue tests for newspapers conforming to GALENP.dtd.
"""

from defoe.papers.issue import Issue
from defoe.file_utils import get_path
from defoe.test.papers import fixtures
from defoe.test.papers.test_issue import TestIssue


class TestIssueGalen(TestIssue):
    """
    defoe.papers.issue.Issue tests for newspapers conforming to
    GALENP.dtd.
    """

    __test__ = True

    def setUp(self):
        """
        Creates Issue from test file fixtures/1912_11_10_galen.xml.
        """
        self.filename = get_path(fixtures, '1912_11_10_galen.xml')
        self.issue = Issue(self.filename)
