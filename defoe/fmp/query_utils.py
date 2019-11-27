"""
Query-related utility functions.
"""

from defoe import query_utils
from defoe.query_utils import PreprocessWordType
from nltk.corpus import words
from PIL import Image
from pathlib import Path
import os

def get_page_matches(document,
                     keywords,
                     preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:
        (<YEAR>, <DOCUMENT>, <PAGE>, <KEYWORD>)
    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.
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
    for keyword in keywords:
        for page in document:
            match = None
            for word in page.words:
                preprocessed_word = query_utils.preprocess_word(
                    word, preprocess_type)
                if preprocessed_word == keyword:
                    match = (document.year, document, page, keyword)
                    break
            if match:
                matches.append(match)
                continue  # move to next page
    return matches

def get_article_matches(document,
                        keywords,
                        preprocess_type=PreprocessWordType.LEMMATIZE):
    """
        (<YEAR>, <DOCUMENT>, <ARTICLE>, <BLOCK_ID>, <COORDENATES>, <PAGE_AREA>, <ORIGINAL_WORDS>,<PREPROCESSED_WORDS>, <PAGE_NAME>, <KEYWORDS> )
    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.
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
    for keyword in keywords:
        for article in document_articles:
            for tb in document_articles[article]:
                 match = None
                 tb_preprocessed_words=[]
                 for word in tb.words:
                     preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
                     tb_preprocessed_words.append(preprocessed_word)
                 for preprocessed_word in tb_preprocessed_words:
                     if preprocessed_word == keyword:
                         match = (document.year, document, article, tb.textblock_id, tb.textblock_coords, tb.textblock_page_area, tb.words, tb_preprocessed_words, tb.page_name, keyword)
                         break
                 if match:
                     matches.append(match)
                     continue  # move to next article
    return matches


def get_tb_matches(target_match,keywords):
    """
    (target_match=><YEAR>, <DOCUMENT>, <ARTICLE>, <BLOCK_ID>, <COORDENATES>, <PAGE_AREA>, <ORIGINAL_WORDS>,<PREPROCESSED_WORDS>, <PAGE_NAME>, <TARGETWORD>)
    :param document: target_match
    :type document: list
    :param keywords: keywords
    :type keywords: list(str or unicode:
    :return: list of tuples
    :rtype: list(tuple)
    """
    
    year, document, article, textblock_id, textblock_coords, textblock_page_area, words, tb_preprocessed_words, page_name, target = target_match
    matches = []
    for keyword in keywords:
        match = None
        for preprocessed_word in tb_preprocessed_words:
            if preprocessed_word == keyword:
                match = (year, document, article, textblock_id, textblock_coords, textblock_page_area, words, tb_preprocessed_words, page_name, keyword, target)
                break
        if match:
            matches.append(match)
            continue  # move to next article
    return matches

def segment_image(coords, page_name, issue_path, keyword, output_path, target=""):
    """
    Segments texblock articles given coordenates and page path
    :param coords: coordenates of an image
    :type coords: string
    :param page_name: name of the page XML which the texblock has been extracted from.
    :type page_name: string
    :param issue_path: path of the ZIPPED archive/issue
    :type issue_path: string
    :param year: year of the publication
    :type year: integer
    :param keyword: word for which the textblock has been selected/filtered 
    :type keyword: string
    :param output_path: path to store the cropped image
    :type output_path: string
    :return: list of images cropped/segmented
    """
    
    if ".zip" in issue_path:  
       image_path=os.path.split(issue_path)[0]
    else:
       image_path=issue_path

    image_name=Path(page_name).stem
    image=Path(image_path, image_name+".jp2")
       
    coords_list=coords.split(",")
    c_set = tuple([int(s) for s in coords_list])
    coords_name=coords.replace(",", "_")

    fname = Path(image).stem
    if target:
        filename = f'crop_{fname}_{target}_{keyword}_{coords_name}.jpg'
    else:
        filename = f'crop_{fname}_{keyword}_{coords_name}.jpg'

    out_file = os.path.join(output_path, filename)
    im = Image.open(image)
    crop = im.crop(c_set)
    crop.save(out_file, quality=80, optimize=True)
    return out_file


def get_document_keywords(document,
                          keywords,
                          preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets list of keywords occuring within an document.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: sorted list of keywords that occur within article
    :rtype: list(str or unicode)
    """
    matches = set()
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if preprocessed_word in keywords:
                matches.add(preprocessed_word)
    return sorted(list(matches))


def document_contains_word(document,
                           keyword,
                           preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Checks if a keyword occurs within an article.

    :param article: Article
    :type article: defoe.papers.article.Article
    :param keywords: keyword
    :type keywords: str or unicode
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: True if the article contains the word, false otherwise
    :rtype: bool
    """
    for page in document:
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word,
                                                            preprocess_type)
            if keyword == preprocessed_word:
                return True
    return False


def calculate_words_within_dictionary(page, 
                   preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Calculates the % of page words within a dictionary and also returns the page quality (pc)
    Page words are normalized. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: matches
    :rtype: list(str or unicode)
    """
    dictionary = words.words()
    counter= 0
    total_words= 0
    for word in page.words:
         preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
         if preprocessed_word!="":
            total_words += 1
            if  preprocessed_word in dictionary:
               counter +=  1
    try:
       calculate_pc = str(counter*100/total_words)
    except:
       calculate_pc = "0" 
    return calculate_pc

def calculate_words_confidence_average(page):
    """
    Calculates the average of "words confidence (wc)"  within a page.
    Page words are normalized. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: matches
    :rtype: list(str or unicode)
    """
    dictionary = words.words()
    counter= 0
    total_wc= 0
    for wc in page.wc:
               total_wc += float(wc)
    try:
       calculate_wc = str(total_wc/len(page.wc))
    except:
       calculate_wc = "0" 
    return calculate_wc

