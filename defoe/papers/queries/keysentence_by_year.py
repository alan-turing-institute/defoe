"""
Counts number of occurrences of keysentences and groups by year.
"""

from operator import add

from defoe import query_utils
from defoe.papers.query_utils import get_article_as_string, get_sentences_list_matches

"""
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); (other value) original word. 
"""
prep_type= 0


def do_query(issues, config_file=None, logger=None):
    """
    Counts number of articles that appears any of the keysentences and groups by year.

    config_file must be the path to a configuration file with a list
    of the keysentences to search for, one per line.

    Both sentences and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        <YEAR>:
        - [<SENTENCE>, <NUM_ARTICLES>]
        - [<SENTENCE>, <NUM_ARTICLES>]
        - ...
        <YEAR>:
        ...

    :param issues: RDD of defoe.papers.issue.Issue
    :type issues: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keysentences grouped by year
    :rtype: dict
    """
    keysentence = []
    with open(config_file, "r") as f:
        for k_sentence in list(f):
            k_split=k_sentence.split()
            sentence_word = [query_utils.preprocess_word(word, prep_type) for word in k_split]
            sentence_norm=''
            for word in sentence_word:
               if sentence_norm == '' :
                   sentence_norm = word
               else:
                   sentence_norm+=" "+ word
            keysentence.append(sentence_norm)
    # [(year, article_string)
    articles = issues.flatMap(
        lambda issue: [(issue.date.year, get_article_as_string(article)) for article in issue.articles])
    
    # [(year, article_string)
    filter_articles = articles.filter(
          lambda year_count: any(k_sentence in year_count[1] for k_sentence in keysentence))
    
   # [(year, [k_sentence, k_sentence]), ...]
    matching_articles = filter_articles.map(
          lambda year_article:(year_article[0], get_sentences_list_matches(year_article[1], keysentence)))
    
   # [[(year, k_sentence), 1) ((year, k_sentence),1) ] ...]
    matching_sentences = matching_articles.flatMap(
          lambda year_sentence:[((year_sentence[0], sentence), 1) for sentence in year_sentence[1]]) 
  
    # [((year, k_sentence), num_k_sentences), ...]
    # =>
    # [(year, (k_sentence, num_k_sentences)), ...]
    # =>
    # [(year, [k_sentence, num_k_sentences]), ...]
    result = matching_sentences\
         .reduceByKey(add)\
        .map(lambda yearsentence_count:
             (yearsentence_count[0][0],
              (yearsentence_count[0][1], yearsentence_count[1]))) \
        .groupByKey() \
        .map(lambda year_sentencecount:
             (year_sentencecount[0], list(year_sentencecount[1]))) \
        .collect()
    return result

