"""
Read from HDFS file, and counts number of occurrences of keywords or keysentences and groups by year.
"""

from operator import add
from defoe import query_utils
from defoe.hdfs.query_utils import get_sentences_list_matches

import yaml, os

def do_query(df, config_file=None, logger=None, context=None):
    """
    Read from HDFS, and counts number of occurrences of keywords or keysentences and groups by year.
    We have an entry in the HFDS file with the following information: 
    - title, edition, year, place, archive filename, page filename, page id, num pages, type of archive, model, type of preprocess treatment, prep_page_string

    Notice, that year is in position "2", preprocess type in poistion "10",
    and the preprocessed page as an string is in position 11. However, the information per entry has been saved as an string.
    
    Example of one entry saved as string. 
    
       u"('Encyclopaedia Britannica', 'Seventh edition, Volume 13, LAB-Magnetism', '1842', 'Edinburgh', 
       '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica/193108323', 'alto/193201394.34.xml', 
       'Page9', '810', 'book', 'nls', 'PreprocessWordType.NORMALIZE', u'the encyclopaedia britannica dictionary of 
        arts sciences and general literature seventh edition i with preliminary dissertations on the history of the 
        sciences and other extensive improvements and additions including the late supplement a general index and 
        numerous engravings volume xiii adam and charles black edinburgh mdcccxlii')"
    
     Therefore,  we need first to recreate a list per entry by spliting each string. 

       [u"'Encyclopaedia Britannica", u" 'Seventh edition, Volume 13, LAB-Magnetism", u" '1842", u" 'Edinburgh", 
       u" '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica/193108323", u" 'alto/193201394.34.xml", 
       u" 'Page9", u" '810", u" 'book", u" 'nls", u" 'PreprocessWordType.NORMALIZE", u" u'the encyclopaedia britannica dictionary of 
       arts sciences and general literature seventh edition i with preliminary dissertations on the history of the sciences and other extensive improvements 
       and additions including the late supplement a general index and numerous engravings volume xiii adam and charles black edinburgh mdcccxlii'"]
   
    And later, for this query we need to get the year (position 2, and convert it into a integer) 
    ,preprocess type (position 10) and page (position 11). 



    config_file must be the path to a configuration file with a list
    of the keywords to search for, one per line.

    Both keywords/keysentences and words in documents are normalized, by removing
    all non-'a-z|A-Z' characters.

    Returns result of form:

        {
          <YEAR>:
          [
            [<SENTENCE|WORD>, <NUM_SENTENCES|WORDS>],
            ...
          ],
          <YEAR>:
          ...
        }

    :param archives: RDD of defoe.nls.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: number of occurrences of keywords grouped by year
    :rtype: dict
    """
    
    # Reading data from HDFS
    pages_hdfs = context.textFile(hdfs_data) 
    
    # Ignoring the first character '(' and last character ')' of each entry, and spliting by "'," 
    pages = pages_hdfs.map(
       lambda p_string: p_string[1:-1].split("\',")) 
  
    # Cleaning the first ' of each element.  
    pages_clean = pages.map(
      lambda p_entry: [item.split("\'")[1] for item in p_entry]) 

    # Getting the preprocess type from the first entry - position 10.
    f_entry=pages_clean.take(1) 
    preprocess_type = f_entry[0][10]
    
    with open(config_file, "r") as f:
        config = yaml.load(f)
    
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    keysentences = []
    with open(data_file, 'r') as f:
        for keysentence in list(f):
            k_split = keysentence.split()
            sentence_word = [query_utils.preprocess_word(
                word, preprocess_type) for word in k_split]
            sentence_norm = ''
            for word in sentence_word:
                if sentence_norm == '':
                    sentence_norm = word
                else:
                    sentence_norm += " " + word
            keysentences.append(sentence_norm)
    
     
    filter_pages = pages_clean.filter(
        lambda year_page: any(
            keysentence in year_page[11] for keysentence in keysentences))
    
    
    # [(year, [keysentence, keysentence]), ...]
    # We also need to convert the string as an integer spliting first the '.
    matching_pages = filter_pages.map(
        lambda year_page: (int(year_page[2]),
                              get_sentences_list_matches(
                                  year_page[11],
                                  keysentences)))
    

    # [[(year, keysentence), 1) ((year, keysentence), 1) ] ...]
    matching_sentences = matching_pages.flatMap(
        lambda year_sentence: [((year_sentence[0], sentence), 1)
                               for sentence in year_sentence[1]])


    # [((year, keysentence), num_keysentences), ...]
    # =>
    # [(year, (keysentence, num_keysentences)), ...]
    # =>
    # [(year, [keysentence, num_keysentences]), ...]
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
