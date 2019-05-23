"""
defoe.papers.issue.Issue tests for newspapers conforming to
bl_ncnp_issue_apex.dtd.
"""

from defoe.papers.issue import Issue
from defoe.file_utils import get_path
from defoe.test.papers import fixtures
from defoe.test.papers.test_issue import TestIssue


class TestIssueBl(TestIssue):
    """
    defoe.papers.issue.Issue tests for newspapers conforming to
    bl_ncnp_issue_apex.dtd.
    """

    __test__ = True

    def setUp(self):
        """
        Creates Issue from test file fixtures/1912_11_10_bl.xml.
        """
        self.filename = get_path(fixtures, '1912_11_10_bl.xml')
        self.issue = Issue(self.filename)
        self.issue_id = "NID123_19121110"
