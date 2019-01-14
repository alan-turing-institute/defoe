"""
A module to query files for counts of interesting words. This returns
the number of occurances of each of the target words for each year.
"""

from operator import add

import regex as re


def do_query(issues, interesting_words_file, _):
    """
    Get the count of specific words of interest by year
    """
    interesting_words = [re.compile(r'\b' + word.strip() + r'\b', flags=re.I | re.U)
                         for word in list(open(interesting_words_file))]

    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year, article) for
                                             article in issue.articles])
    # For each article, count how often each word appears in it
    interest = articles.flatMap(words_per_article(interesting_words))

    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .reduceByKey(add) \
        .map(split_key) \
        .groupByKey() \
        .map(snd_to_list) \
        .collect()
    return interesting_by_year


def words_per_article(interesting_words):
    """
    Create a function to count how often each word appears in each article
    """
    def search(year_article):
        """
        Count how often each wor appears in each article
        """
        year, article = year_article
        return [((year, regex.pattern.replace(r'\b', '')),
                 len(regex.findall(article.words_string)))
                for regex in interesting_words]
    return search


def snd_to_list(tup):
    """
    Given a tuple, make the second element a list
    """
    fst, snd = tup
    return (fst, list(snd))


def split_key(tup):
    """
    Given a tuple ((a,b), c) change it to (a, (b,c))
    """
    left, third = tup
    fst, snd = left
    return (fst, (snd, third))
