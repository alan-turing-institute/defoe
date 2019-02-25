"""
Counts number of times that each keyword (or its pre-processed versions -> stemming/lemmatization ) 
appear for every article that has the target word (or its stemming/lemmatization version) in it.
"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word
from defoe.papers.query_utils import get_article_keywords

"""
PREPROCESSING OPTIONS:
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); original word (3). 
"""
prep_type= 2

def do_query(issues, config_file=None, logger=None):
    """
    Counts number of times that each term (or their pre-processed versions -> stemming/lemmatization ) 
    appear for every article that has the target word (or its stemming/lemmatization version) in it.

    config_file must be the path to a configuration file with a target
    word and a list of one or more keywords to search for, one per
    line.

    Target word, keywords and words in documents are preprocessed, using one of the above options.

    Returns result of form:
        <YEAR>:
        - [<WORD>, <NUM_WORDS>]
        - [<WORD>, <NUM_WORDS>]
        - ...
        <YEAR>:


    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped by year
    :rtype: dict
    """
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
   
    # [((year, word), 1), ...]
    words = target_articles.flatMap(
        lambda target_article: [
            ((target_article[0], query_utils.preprocess_word(word,prep_type)), 1)
            for word in target_article[1].words
        ])
    
    # [((year, word), 1), ...]
    matching_words = words.filter(
        lambda yearword_count: yearword_count[0][1] in keywords)
    # [((year, word), num_words), ...]
    # =>
    # [(year, (word, num_words)), ...]
    # =>
    # [(year, [word, num_words]), ...]
    result = matching_words \
        .reduceByKey(add) \
        .map(lambda yearword_count:
             (yearword_count[0][0],
              (yearword_count[0][1], yearword_count[1]))) \
        .groupByKey() \
        .map(lambda year_wordcount:
             (year_wordcount[0], list(year_wordcount[1]))) \
        .collect()
    return result
