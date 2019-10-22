"""
Gets concordance and collocation for keywords selecting only the pages which have occurences of the target word,  and groups the results by date.
This query detects also the sentences in which keywords appear, and preprocess each word of each sentence with different methods. 
"""
import os.path
import yaml
from defoe import query_utils
from defoe.nls.query_utils import extract_sentences, total_preprocessed
from defoe.nls.query_utils import PreprocessWordType
from defoe.query_utils import PreprocessWordType

def do_query(archives, config_file=None, logger=None, context=None):
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

    :param archives: RDD of defoe.nls.archive.Archive
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
    # [document, ...]
    documents = archives.flatMap(
        lambda archive: [document for document in list(archive)])

    # [(year, sentences), ...]
    raw_sentences = documents.flatMap(
        lambda document: extract_sentences(document))

    # [(year, [preprocess_sentences]), (year, [preprocessed_sentence] ) , ...]
    preprocessed_sentences = raw_sentences.flatMap(
        lambda raw_sentences: [total_preprocessed(raw_sentences)])
    
    print("Preprocessed  %s" % preprocessed_sentences.take(3))
    
    # [[year, [preprocess sentence],[preprocess sentence], year, []], ...]
    result = preprocessed_sentences.groupByKey() \
             .map(lambda year_wordcount:
              (year_wordcount[0], list(year_wordcount[1]))) \
            .collect()
    
 
    return result
