"""
This query filters articles’ textblocks by selecting the ones that have one of the target word(s) AND any the keywords.
Later it produces the segmentation/crop or the filtered texblocks. 
"""

from defoe import query_utils
from defoe.fmp.query_utils import get_article_matches, segment_image, get_tb_matches
import yaml
import os


def do_query(archives, config_file=None, logger=None, context=None):
    """
    Crops articles' images for keywords and groups by word.

    Config_file must a yml file that has the following values:
        * preprocess: Treatment to use for preprocessing the words. Options: [normalize|stem|lemmatize|none]
        * data: TXT file with a list of the keywords to search for, one per line. 
                This should be in the same path at the configuration file.

        Important!! : The first two words in this list are treated as targetwords.

        *years_filter: Min and Max years to filter the data. Separeted by "-"
        *output_path: The path to store the cropped images.

    Returns result of form:

        {
          <WORD>:
          [
            { "article_id": <ARTICLE ID>,
              "issue_filename": <ISSUE.ZIP>, 
              "issue_id": <ISSUE ID>
              "coord": <COORDENATES>,
              "cropped_image": <IMAGE.JPG> 
              "page_area": <PAGE AREA>,
              "page_filename": < PAGE FILENAME>,
              "place": <PLACE>,
              "textblock_id": <TEXTBLOCK ID>,
              "title": <TITLER>,
              "words": <WORDS>,
              "preprocessed_words": <PREPROCESSED WORDS> 
              "year": <YEAR>,
              "date": <DATE>
            },
            ...
          ],
          <WORD>:
          ...
        }
    :param archives: RDD of defoe.fmp.archive.Archive
    :type archives: pyspark.rdd.PipelinedRDD
    :param config_file: query configuration file
    :type config_file: str or unicode
    :param logger: logger (unused)
    :type logger: py4j.java_gateway.JavaObject
    :return: information on documents in which keywords occur grouped
    by word
    :rtype: dict
    """
    with open(config_file, "r") as f:
        config = yaml.load(f)
    preprocess_type = query_utils.extract_preprocess_word_type(config)
    data_file = query_utils.extract_data_file(config,
                                              os.path.dirname(config_file))
    year_min, year_max=query_utils.extract_years_filter(config)
    output_path = query_utils.extract_output_path(config)
    keywords = []
    with open(data_file, 'r') as f:
        keywords = [query_utils.preprocess_word(word, preprocess_type)
                    for word in list(f)]

    
    #We can change the following line, if we want to include more or less words as target_words.
    #In this case, the first two words of the lexicon are selected as target_words
    target_words = keywords[0:2]
    #The rest of words of the lexicon are selected as keywords
    keywords = keywords[2:]
    # [document, ...]

    # We will select/filter the texblocks that follows this rule: The text contains at least one target words AND one keyword. 
    

    documents = archives.flatMap(
        lambda archive: [document for document in list(archive) if document.year >= int(year_min) and document.year <= int(year_max) ])

    filtered_tb = documents.flatMap(
        lambda document: get_article_matches(document, target_words, preprocess_type))
    
    filtered_words = filtered_tb.flatMap(lambda tb: get_tb_matches(tb, keywords))

    #[(year, document, article, textblock_id, textblock_coords, textblock_page_area, words, preprocessed_words, page_name, keyword,target), ....]
    # [(word, {"article_id": article_id, ...}), ...]
    matching_docs = filtered_words.map(
        lambda document_article_word:
        (document_article_word[9],
         {"title": document_article_word[1].title,
          "place": document_article_word[1].place,
          "article_id": document_article_word[2],
          "textblock_id": document_article_word[3], 
          "coord": document_article_word[4],
          "page_area": document_article_word[5],
          "year": document_article_word[0],
          "words":  document_article_word[6],
          "date":  document_article_word[1].date,
          "preprocessed_words":  document_article_word[7],
          "page_filename":  document_article_word[8],
          "issue_id": document_article_word[1].documentId,
          "issue_dirname": document_article_word[1].archive.filename,
          "target_word": document_article_word[10],
          "cropped_image": segment_image(document_article_word[4], document_article_word[8], document_article_word[1].archive.filename, document_article_word[9], output_path, document_article_word[10])
         }))


    # [(word, {"article_id": article_id, ...}), ...]
    # =>
    # [(word, [{"article_id": article_id, ...], {...}), ...)]
    result = matching_docs \
        .groupByKey() \
        .map(lambda word_context:
             (word_context[0], list(word_context[1]))) \
        .collect()
    return result
