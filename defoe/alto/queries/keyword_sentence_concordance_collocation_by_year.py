"""
Gets concordance and collocation for keywords selecting only the pages which have occurences of the target word,  and groups the results by date.
This query detects also the sentences in which keywords appear, and preprocess each word of each sentence with different methods. 
"""
import os.path
import yaml
from defoe import query_utils
from defoe.alto.query_utils import get_page_matches, get_sentence_concordance, get_page_sentences, get_sentence_preprocessed
from defoe.alto.query_utils import PreprocessWordType
from defoe.query_utils import PreprocessWordType

def do_query(archives, config_file=None, logger=None):
    """
    Gets concordance and collocation analysis for keywords giving a target word,  and it groups the results by date.
    The window variable can be used for specifying the number of words to the right and left to take. 
  
 
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
    with open(config_file, "r") as f:
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    with open(data_file, "r") as f:
        keywords = [query_utils.preprocess_word(word, PreprocessWordType.NORMALIZE) for word in list(f)]
    target_word =[]
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
    # [(year, pace), ...]
    target_docs = filtered_words.map(
        lambda year_document_page_word:
        (year_document_page_word[0], year_document_page_word[2]))
    

    # [(year, (page, [(word, sentence), (word, sentence) ...]), ...]
    matching_sentences = target_docs.map(
        lambda year_doc: (
            (year_doc[0],
             get_page_sentences(year_doc[1], keywords))))
    # [(year, (word, corcondance), (word, concordance) ...), ...]
    concordance_words = matching_sentences.flatMap(
        lambda target_doc: [
            (target_doc[0], get_sentence_preprocessed(match))
            for match in target_doc[1][1]])
    
    # [(year, [word, concodance], [word, concordance]), ...]
    result = concordance_words.groupByKey() \
             .map(lambda year_wordcount:
              (year_wordcount[0], list(year_wordcount[1]))) \
            .collect()
    return result
