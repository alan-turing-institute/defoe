"""
Gets concordance for keywords and groups by date.
"""

from defoe import query_utils
from defoe.papers.query_utils import get_article_matches
from defoe.papers.query_utils import PreprocessWordType


def do_query(issues, config_file=None, logger=None):
    """
    Gets concordance for keywords and groups by date.

    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <DATE>:
          [
            {
              "title": <TITLE>,
              "page_ids": <PAGE_IDS>,
              "content": <PAGE_CONTENT>,
              "word": <WORD>,
              "article_id": <ARTICLE_ID>,
              "issue_id": <ISSUE_ID>,
              "filename": <FILENAME>
            },
            ...
          ],
          <DATE>:
          ...
        }

    :param issues: RDD of defoe.alto.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by date
    :rtype: dict
    """
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.normalize(word) for word in list(f)]

    # [(date, issue, article, word), ...]
    filtered_words = issues.flatMap(
        lambda issue: get_article_matches(issue,
                                          keywords,
                                          PreprocessWordType.NORMALIZE))

    # [(date, issue, article, word), ...]
    # =>
    # [(date, {"title": title, ...}), ...]
    matching_docs = filtered_words.map(
        lambda date_issue_article_word:
        (date_issue_article_word[0],
         {"title": date_issue_article_word[2].title_string,
          "page_ids": list(date_issue_article_word[2].page_ids),
          "content": date_issue_article_word[2].words_string,
          "word": date_issue_article_word[3],
          "article_id": date_issue_article_word[2].article_id,
          "issue_id": date_issue_article_word[1].newspaper_id,
          "filename": date_issue_article_word[1].filename}))

    # [(date, {"title": title, ...}), ...]
    # =>
    # [(date, [{"title": title, ...], {...}), ...)]
    result = matching_docs \
        .groupByKey() \
        .map(lambda date_context:
             (date_context[0], list(date_context[1]))) \
        .collect()
    return result
