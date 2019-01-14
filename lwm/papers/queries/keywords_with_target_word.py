"""
Identify counts of articles that contain a keyword, and a given
second keyword.

The first keyword in the file is the keyword that must be in all the
documents. The rest of the words are individually checked.
"""

from operator import add

import regex as re


def do_query(issues, interesting_words_file, _):
    """
    Get the words which appear together in articles.
    """
    # Get the list of words to search for
    all_words = [re.compile(r'\b' + word.strip() + r'\b', re.I | re.U)
                 for word in list(open(interesting_words_file))]
    match_word = all_words[0]
    keywords = all_words[1:]
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year,
                                              article) for
                                             article in
                                             issue.articles])
    # Find the relevant articles, and the words they match
    interest = articles. \
        filter(filter_on(match_word)). \
        flatMap(make_search(keywords))
    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(add) \
        .map(split_key) \
        .groupByKey() \
        .map(snd_to_list) \
        .collect()
    return interesting_by_year


def filter_on(keyword):
    """
    Return a function that can filter based on a given keyword
    """
    def filter_on_word(year_article):
        """
        Given a tuple of year and article, return true if the
        article contains the given regex
        """
        _, article = year_article
        return keyword.findall(article.words_string)
    return filter_on_word


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
        matched_words = [((year, regex.pattern.replace(r'\b', '').lower()), 1)
                         for regex in interesting_words if
                         regex.findall(article.words_string)]
        if matched_words == []:
            matched_words = [((year, 'N/A'), 1)]
        return matched_words
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
