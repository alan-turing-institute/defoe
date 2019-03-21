"""
Gets concordance and collocation for keywords selecting only the pages which have occurences of the target word,  and groups the results by date.
"""

from defoe import query_utils
from defoe.alto.query_utils import get_page_matches, get_page_idx, get_concordance

"""
PREPROCESSING OPTIONS:
prep_type: integer variable, which indicates the type of preprocess treatment
to appy to each word. normalize(0); normalize + stemming (1); normalize + lemmatization (2); (other value) original word. 
"""
prep_type= 2

def do_query(archives, config_file=None, logger=None):
    """
    Gets concordance and collocation analysis for keywords giving a target word,  and it groups the results by date.
    The window variable can be used for specifying the number of words to the right and left to take. 
    (e.g. 5 words to the left and right, including sentence boundaries).
  
 
    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.
    Keywords and words in documents are preprocessed, using one of the above options.
     Returns result of form:
        <YEAR>:
        - [<WORD>, <CONCORDANCE>]
        - [<WORD>, <CONCORDANCE>]

    :param archives: RDD of defoe.alto.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by year
    :rtype: dict
    """
    keywords = []
    window = 10
    with open(config_file, "r") as f:
        keywords = [query_utils.preprocess(word,prep_type) for word in list(f)]
    target_word = []
    target_word.append(keywords[0])
    # [document, ...]
    documents = archives.flatMap(
        lambda archive: [document for document in list(archive)])

    # [(year, document, page, word), ...]
    filtered_words = documents.flatMap(
        lambda document: get_page_matches(document,
                                           target_word))

    # [(year, document, page, word), ...]
    # =>
    # [(year, pace.content), ...]
    target_docs = filtered_words.map(
        lambda year_document_page_word:
        (year_document_page_word[0], year_document_page_word[2]))

    # [(year, (page, [(word, idx), (word, idx) ...]), ...]
    matching_idx = target_docs.map(
        lambda year_doc: (
            (year_doc[0],
             get_page_idx(year_doc[1], keywords))))

    # [(year, (word, corcondance), (word, concordance) ...), ...]
    concordance_words = matching_idx.flatMap(
        lambda target_doc: [
            (target_doc[0], get_concordance(target_doc[1][0], match, window))
            for match in target_doc[1][1]])
    
    # [(year, [word, concodance], [word, concordance]), ...]
    result = concordance_words.groupByKey() \
             .map(lambda year_wordcount:
              (year_wordcount[0], list(year_wordcount[1]))) \
            .collect()
    return result
