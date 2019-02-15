"""
Counts total number of issues, articles and words per year.

This can be useful if wanting to see how the average number of
issues, articles and words change over time, for example.
"""


def do_query(issues, config_file=None, logger=None):
    """
    Counts total number of issues, articles and words per year.

    Returns result of form:

        {
          <YEAR>: [<NUM_ISSUES>, <NUM_ARTICLES>, <NUM_WORDS>],
          ...
        }

    :param issues RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file (unused)
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: total number of issues, articles and words per year
    :rtype: list
    """
    # [(year, (1, num_articles, num_words))]
    counts = issues.flatMap(
        lambda issue: [(issue.date.year, get_num_articles_words(issue))])
    result = counts \
        .reduceByKey(lambda x, y:
                     tuple(i + j for i, j in zip(x, y))) \
        .map(lambda year_data: (year_data[0], list(year_data[1]))) \
        .collect()
    return result


def get_num_articles_words(issue):
    """
    Give an issue, gets a tuple with the number of articles and total
    number of words in the articles.

    :param issue: issue
    :type issue: defoe.papers.issue.Issue
    :return: (1, num_articles, num_words)
    :rtype: tuple(int, int, int)
    """
    num_words_per_article = [len(article.words)
                             for article in issue.articles]
    num_words = sum(num_words_per_article)
    return (1, len(issue.articles), num_words)
