"""
Gets concordance and collocation for keywords and groups by date.
"""

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word, get_article_idx, get_concordance

"""
PREPROCESSING OPTIONS:
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); (other value) original word. 
"""
prep_type= 3

def do_query(issues, config_file=None, logger=None):
    """
    Gets concordance and collocation analysis for keywords and groups by date.
    The variable window can be used for specified how many words to take. 
    (e.g. 5 words to the left and right, including sentence boundaries).
  
 
    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Keywords and words in documents are preprocessed, using one of the above options.


    Returns result of form:
        <YEAR>:
        - [<WORD>, <CONCORDANCE>]
        - [<WORD>, <CONCORDANCE>]

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
    
    window = 5
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.preprocess_word(word, prep_type) for word in list(f)]
    target_word = keywords[0]
    # [(year, article), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, article)
                       for article in issue.articles])
    # [(year, article), ...]
    target_articles = articles.filter(
        lambda year_article: article_contains_word(
            year_article[1], target_word))

    # [(year, (article, [(word, idx), (word, idx) ...]), ...]
    matching_idx = target_articles.map(
        lambda year_article: (
            (year_article[0],
             get_article_idx(year_article[1], keywords))
            ))
   # [(year, (word, corcondance), (word, concordance) ...), ...]
    concordance_words = matching_idx.flatMap(
        lambda target_article: [
            (target_article[0], get_concordance(target_article[1][0], match, window))
            for match in target_article[1][1]])
    
    # [(year, [word, concodance], [word, concordance]), ...]

    result = concordance_words.groupByKey() \
             .map(lambda year_wordcount:
              (year_wordcount[0], list(year_wordcount[1]))) \
            .collect()
    return result

