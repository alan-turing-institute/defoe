'''
This module returns the full XML of the articles that contain
a given regular expression.
'''

import re
from lxml import etree  # pylint: disable=all


def do_query(issues, interesting_words_file, _log):
    '''
    Get the count of specific words of interest by year
    '''
    # Get the list of words to search for
    regex_string = r'\b('
    first = True
    for word in list(open(interesting_words_file)):
        if not first:
            regex_string = regex_string + r'|'
        regex_string = regex_string + word.strip()
        first = False
    regex_string = regex_string + r')\b'

    interesting_words = re.compile(regex_string, re.I | re.U)
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date, article) for
                                             article in issue.articles])
    # Add 1 record for each word that appears in each article in each year
    interest = articles.flatMap(lambda (date, article):
                                check_text(date, article, interesting_words))

    # Group elements by year
    interesting_by_year = interest \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    return interesting_by_year


def check_text(date, article, interesting_words):
    '''
    Catch articles that match the given regex
    '''
    if interesting_words.search(article.words_string) is not None:
        return [(date, etree.tostring(article.tree))]
    return []
