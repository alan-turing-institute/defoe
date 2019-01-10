"""
A module to query files to find every word used in the TDA and its frequency
"""

from operator import add
from random import uniform


ACCEPTANCE_PROBABILTY = 0.2


def do_query(issues, _in, _log):
    """
    Count each word that occurs in the archive
    """
    # Break out each article from each issue
    articles = issues.flatMap(lambda issue: [article for
                                             article in issue.articles])
    # Break out each word from each article
    words = articles.flatMap(lambda article: [(str(word), 1) for
                                              word in article.words])

    # Now add sum the word counts
    word_counts = words. \
        reduceByKey(add). \
        map(fix_counts). \
        collect()
    return word_counts


def fix_counts(record):
    """
    Fix the record counts based on the acceptance
    probability
    """
    word, count = record
    factor = 1.0 / ACCEPTANCE_PROBABILTY
    return (word, int(count * factor))


def count_words_in_article(words):
    """
    Count the number of times each word appears.
    To deal with the long tail of unique words, roll a dice
    before allowing a word in
    """
    counts = {}
    for word in words:
        if uniform(0, 1) > ACCEPTANCE_PROBABILTY:
            continue
        count = counts.get(word)
        if count is None:
            counts[word] = 1
        else:
            counts[word] = count + 1
    return [(word, count) for word, count in counts.items()]
