"""
Gets contextual information about the occurences of words and
group by year.

The query expects a file with a list of the words to search for, one
per line.

The result is of form, for example:

    YEAR:
    - { "filename": FILENAME,
        "newspaper_id": NEWSPAPER_ID,
        "article_title": TITLE,
        "article_id": ARTICLE_ID,
        "page_ids": [PAGE_ID, PAGE_ID, ...],
        "text": TEXT }
    - { ... }
    ...
    YEAR:
    ...
"""

import re


def do_query(issues, words_file, logger=None):
    """
    Gets contextual information about the occurences of words
    and group by year.

    :param archives: Archives holding Documents
    :type archives: pyspark.rdd.PipelinedRDD with Archives.
    :param words_file: File with list of words to search for,
    one per line
    :type words_file: str or unicode
    :param: logger: Logger
    :return: query results
    """
    # Get the list of words to search for
    words_regex_str = r'\b('
    first = True
    for word in list(open(words_file)):
        if not first:
            words_regex_str = words_regex_str + r'|'
        words_regex_str = words_regex_str + word.strip()
        first = False
    words_regex_str = words_regex_str + r')\b'

    words_regex = re.compile(words_regex_str, re.I | re.U)

    # Map each article in each issue to its year of publication
    articles = issues.flatMap(lambda issue: [(issue.date,
                                              issue,
                                              article) for
                                             article in issue.articles])
    # Add one record for each word that appears in each article in
    # each year
    interest = articles.flatMap(lambda (date,
                                        issue,
                                        article):
                                check_text(date,
                                           issue,
                                           article,
                                           words_regex))
    # Group elements by year
    interesting_by_year = interest \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    return interesting_by_year


def check_text(date, issue, article, words_regex):
    """
    Catch articles that match the given regex.

    A list with a tuple of the following form is returned

        (DATE,
         {
           "filename": FILENAME,
           "newspaper_id": NEWSPAPER_ID,
           "article_title": TITLE,
           "article_id": ARTICLE_ID,
           "page_ids": [PAGE_D, PAGE_ID, ...],
           "text": TEXT
          }
        )

    :param date: Issue publication date
    :type date: datetime
    :param issue: Issue to which article belongs
    :type issue: defoe.papers.issue.Issue
    :param article: Article
    :type article: defoe.papers.article.Article
    :param words_regex: Regular expression with words to search for
    :type words_regex: _sre.SRE_Pattern
    :return: list with a tuple if the article's text matches the
    given regular expression
    :rtype: list of tuple(str or unicode, list)
    """
    if words_regex.search(article.words_string) is not None:
        return [(date.date(),
                 {
                     "newspaper_id": issue.newspaper_id,
                     "filename": issue.filename,
                     "article_title": " ".join(article.title),
                     "article_id": str(article.article_id),
                     "page_ids": article.page_ids,
                     "text": article.words_string
                 })]
    return []
