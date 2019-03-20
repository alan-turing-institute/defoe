"""
Gets concordance and collocation for keywords selecting only the articles which have occurences of the target word,  and groups the results by date.
"""

from defoe import query_utils
from defoe.papers.query_utils import article_contains_word, get_article_idx, get_concordance

"""
PREPROCESSING OPTIONS:
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); (other value) original word. 
"""
prep_type= 2

def do_query(issues, config_file=None, logger=None):
    """
    Gets concordance and collocation analysis for keywords giving a target word,  and it groups the results by date.
    The window variable can be used for specifying the number of words to the right and left to take. 
    (e.g. 5 words to the left and right, including sentence boundaries).
  
 
    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Keywords and words in documents are preprocessed, using one of the above options.


    Returns result of form:
        <YEAR>:
        - [<FILENAME>, <WORD>, <CONCORDANCE>]
        - [<FILENAME>, <WORD>, <CONCORDANCE>]

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
    
    window = 10
    keywords = []
    with open(config_file, "r") as f:
        keywords = [query_utils.preprocess_word(word, prep_type) for word in list(f)]
    target_word = keywords[0]
    # [(year, issue, article, ocr), ...]
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, issue.filename, article, article.quality)
                       for article in issue.articles])
    # [(year, filename, article, ocr), ...]
    target_articles = articles.filter(
        lambda year_article: article_contains_word(
             year_article[2], target_word))


    # [(year, (article, filename, ocr [(word, idx), (word, idx) ...]), ...]
    matching_idx = target_articles.map(
        lambda year_article: (
            (year_article[0],
             get_article_idx(year_article[1],year_article[2], keywords, year_article[3]))
            ))

   # [(year, (filename, word, corcondance, ocr), (filename, word, concordance, ocr) ...), ...]
    concordance_words = matching_idx.flatMap(
        lambda target_article: [
            (target_article[0], get_concordance(target_article[1][0],target_article[1][1], match, window, target_article[1][3]))
            for match in target_article[1][2]])
    
    
    # [(year, [filename, word, concodance, ocr], [filename, word, concordance, ocr]), ...]

    result = concordance_words.groupByKey() \
             .map(lambda year_wordcount:
              (year_wordcount[0], list(year_wordcount[1]))) \
            .collect()
    return result

