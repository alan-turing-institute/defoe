"""
This module finds which words are contained together in articles.
"""

from operator import add

import regex as re


def do_query(issues, interesting_words_file, _):
    """
    Get the words which appear together in articles.
    """
    # Get the list of words to search for
    interesting_words = [re.compile(r'\b' + word.strip() + r'\b', re.I | re.U)
                         for word in list(open(interesting_words_file))]
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year,
                                              article) for
                                             article in
                                             issue.articles])
    # Find the words for each article
    interest = articles.flatMap(make_search(interesting_words))
    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(add) \
        .map(split_key) \
        .groupByKey() \
        .map(snd_to_list) \
        .collect()
    return interesting_by_year


def make_search(interesting_words):
    """
    Make a function to search for the words in the given list
    and return which ones occur in the same article
    """
    def words_in_article(data):
        """
        For every article make a list of words that it has matched in it
        """
        year, article = data
        matched_words = [regex.pattern.replace(r'\b', '').lower()
                         for regex in interesting_words if
                         regex.findall(article.words_string)]
        return [((year, str(sorted(matched_words))), 1)]
    return words_in_article


def split_key(tup):
    """
    Given a tuple ((a,b), c) change it to (a, (b,c))
    """
    left, third = tup
    fst, snd = left
    return (fst, (snd, third))


def snd_to_list(tup):
    """
    Given a tuple, make the second element a list
    """
    fst, snd = tup
    return (fst, list(snd))
