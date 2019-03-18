"""
defoe.papers.article.article tests for newspapers conforming to
bl_ncnp_issue_apex.dtd.
"""

from defoe.papers.issue import Issue
from defoe.file_utils import get_path
from defoe.test.papers import fixtures
from defoe.test.papers.test_article import TestArticle


class TestArticleBl(TestArticle):
    """
    defoe.papers.article.article tests for newspapers conforming to
    bl_ncnp_issue_apex.dtd.
    """

    __test__ = True

    def setUp(self):
        """
        Creates Issue from test file fixtures/1912_11_10_bl.xml then
        retrieves first Article.
        """
        self.filename = get_path(fixtures, '1912_11_10_bl.xml')
        issue = Issue(self.filename)
        self.article = issue.articles[0]
        self.article_id = 'NID123_19121110_0001-001'
