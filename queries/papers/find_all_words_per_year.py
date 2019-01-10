"""
A module to query article counts. This returns
the number of articles per year.
"""

from operator import add


def do_query(issues, _infile, _log):
    """
    Get the total count of words written per year
    """
    # For each article map the date, to its length
    article_lengths = issues.flatMap(lambda issue: [(issue.date.year,
                                                     len(article.words))
                                                    for article in
                                                    issue.articles])
    # Now add sum the word counts
    word_counts = article_lengths \
        .reduceByKey(add) \
        .collect()
    return word_counts
