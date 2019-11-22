"""
This query filters articles’ textblocks by selecting the ones that have one of the target word(s) AND any the keywords.
Later it produces the segmentation/crop or the filtered texblocks. 
"""

from defoe import query_utils
from defoe.fmp.query_utils import segment_image
import yaml
import os
from collections import namedtuple, defaultdict

WordLocation = namedtuple('WordLocation',
                    ("word "
                    "position "
                    "year "
                    "document "
                    "article "
                    "textblock_id "
                    "textblock_coords "
                    "textblock_page_area "
                    "textblock_page_name"))
MatchedWords = namedtuple('MatchedWords', 'target_word keyword textblock distance words preprocessed')

def compute_distance(word1_loc, word2_loc):
    return abs(word1_loc.position - word2_loc.position)

def get_min_distance_to_target(keyword_locations, target_locations):
    min_distance = None
    target_loc = None
    keyword_loc = None
    for k_loc in keyword_locations:
        for t_loc in target_locations:
            d = compute_distance(k_loc, t_loc)
            if not min_distance or d < min_distance:
                min_distance = d
                target_loc = t_loc
                keyword_loc = k_loc
    return min_distance, target_loc, keyword_loc


def find_words(
        document, target_words, keywords,
        preprocess_type=query_utils.PreprocessWordType.LEMMATIZE):
    """
    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.
    The distance between keyword and target word is recorded in the output tuple.
    :param document: document
    :type document: defoe.alto.document.Document
    :param keywords: keywords
    :type keywords: list(str or unicode:
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: list of tuples
    :rtype: list(tuple)
    """
    matches = []
    document_articles=document.articles
    for article in document_articles:
        for tb in document_articles[article]:
            keys = defaultdict(lambda: [])
            targets = []
            preprocessed_words = []
            for pos, word in enumerate(tb.words):
                preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
                loc = WordLocation(
                    word=preprocessed_word,
                    position=pos,
                    year=document.year, 
                    document=document, 
                    article=article, 
                    textblock_id=tb.textblock_id, 
                    textblock_coords=tb.textblock_coords, 
                    textblock_page_area=tb.textblock_page_area, 
                    textblock_page_name=tb.page_name)
                preprocessed_words.append(preprocessed_word)
                if preprocessed_word in keywords:
                    keys[preprocessed_word].append(loc)
                if preprocessed_word in target_words:
                    targets.append(loc)
            for k, l in keys.items():
                min_distance, target_loc, keyword_loc = get_min_distance_to_target(l, targets)
                if min_distance:
                    matches.append(
                        MatchedWords(
                            target_word=target_loc.word,
                            keyword=keyword_loc.word,
                            textblock=target_loc,
                            distance=min_distance,
                            words=tb.words,
                            preprocessed=preprocessed_words
                        )
                    )

    return matches

def do_query(archives, config_file=None, logger=None, context=None):
    """
    Crops articles' images for keywords and groups by word.

    Config_file must a yml file that has the following values:
        * preprocess: Treatment to use for preprocessing the words. Options: [normalize|stem|lemmatize|none]
        * data: yaml file with a list of the target words and a list of keywords to search for.
                This should be in the same path at the configuration file.
        * years_filter: Min and Max years to filter the data. Separeted by "-"
        * output_path: The path to store the cropped images.

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
              "date": <DATE>,
              "distance": <DISTANCE BETWEEN TARGET AND KEYWORD>,
              "total_words": <NUMBER OF WORDS IN TEXTBLOCK>
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
        input_words = yaml.load(f)

    target_words = set([query_utils.preprocess_word(word, preprocess_type) for word in input_words['targets']])
    keywords = set([query_utils.preprocess_word(word, preprocess_type) for word in input_words['keywords']])

    # retrieve the documents from each archive
    documents = archives.flatMap(
        lambda archive: [document for document in archive if int(year_min) <= document.year <= int(year_max) ])

    # find textblocks that contain pairs of (target word, keyword) and record their distance
    filtered_words = documents.flatMap(
        lambda document: find_words(document, target_words, keywords, preprocess_type))
    
    # create the output dictionary
    # mapping from
    #   [MatchedWords(target_word, keyword, textblock_location, distance, words, preprocessed)]
    # to
    #   [(word, {"article_id": article_id, ...}), ...]
    matching_docs = filtered_words.map(
        lambda matched:
        (matched.keyword, {
            "title": matched.textblock.document.title,
            "place": matched.textblock.document.place,
            "article_id": matched.textblock.article,
            "textblock_id": matched.textblock.textblock_id, 
            "coord": matched.textblock.textblock_coords,
            "page_area": matched.textblock.textblock_page_area,
            "year": matched.textblock.year,
            "date":  matched.textblock.document.date,
            # "words": matched.words,
            # "preprocessed_words":  matched.preprocessed,
            "page_filename":  matched.textblock.textblock_page_name,
            "issue_id": matched.textblock.document.documentId,
            "issue_dirname": matched.textblock.document.archive.filename,
            "target_word": matched.target_word,
            "distance": matched.distance,
            "cropped_image": segment_image(
                matched.textblock.textblock_coords, 
                matched.textblock.textblock_page_name, 
                matched.textblock.document.archive.filename, 
                matched.keyword, 
                output_path, 
                matched.target_word)
            }
        ))

    # group by the matched keywords and collect all the articles by keyword
    # [(word, {"article_id": article_id, ...}), ...]
    # =>
    # [(word, [{"article_id": article_id, ...], {...}), ...)]
    # sorted by distance between target and keyword
    result = matching_docs \
        .groupByKey() \
        .map(lambda word_context:
             (word_context[0], sorted(list(word_context[1]), key=lambda d: d['distance']))) \
        .collect()
    return result
