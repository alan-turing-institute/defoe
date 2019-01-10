'''
A module to query article counts. This returns
the number of articles per year.
'''

from operator import add


def do_query(issues, _, _log):
    '''
    Get the count of words by articles by year
    '''
    # For each issue map the date, the number of articles as a key,
    # and the value is each articles length
    articles = issues.flatMap(lambda issue: [(issue.date.year,
                                              len(issue.articles))])
    # Now add sum the article counts
    interesting_by_year = articles \
        .reduceByKey(add) \
        .collect()
    return interesting_by_year
