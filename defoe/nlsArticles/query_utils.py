"""
Query-related utility functions.
"""

from defoe import query_utils
from defoe.query_utils import PreprocessWordType, longsfix_sentence, xml_geo_entities, georesolve_cmd,  coord_xml, geomap_cmd, geoparser_cmd, geoparser_coord_xml
from nltk.corpus import words
import re
import spacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
NON_AZ_REGEXP = re.compile('[^a-z]')




def get_pages_matches_no_prep(title, edition, archive, filename, text, keysentences):
    """
    Get pages within a document that include one or more keywords.
    For each page that includes a specific keyword, add a tuple of
    form:

        (<TITLE>, <EDITION>, <ARCHIVE>, <FILENAME>, <TEXT>, <KEYWORD>)

    If a keyword occurs more than once on a page, there will be only
    one tuple for the page for that keyword.
    If more than one keyword occurs on a page, there will be one tuple
    per keyword.

    :return: list of tuples
    """  
    matches = []
    for keysentence in keysentences:
        sentence_match = get_sentences_list_matches(text, keysentence)
        if sentence_match: 
            match = (title, edition, archive, filename, text, keysentence)
            matches.append(match) 
    return matches



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
    :type document: defoe.nls.document.Document
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
    :type page: defoe.nls.page.Page
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
    :type page: defoe.nls.page.Page
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

def get_page_as_string(page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):
    """
    Return a page as a single string.

    :param page: Page
    :type page: defoe.nls.Page
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: page words as a string
    :rtype: string or unicode
    """
    page_string = ''
    for word in page.words:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string


def clean_page_as_string(page):
        
    """
    Clean a page as a single string,
    Handling hyphenated words: combine and split and also fixing the long-s

    :param page: Page
    :type page: defoe.nls.Page
    :return: clean page words as a string
    :rtype: string or unicode
    """
    page_string = ''
    for word in page.words:
        if page_string == '':
            page_string = word
        else:
            page_string += (' ' + word)

    page_separete = page_string.split('- ')
    page_combined = ''.join(page_separete)
   
    if (len(page_combined) > 1) and ('f' in page_combined): 
       page_clean = longsfix_sentence(page_combined) 
       return page_clean
    else:
        return page_combined

def preprocess_clean_page(clean_page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_page.split(' ') 
    page_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string

def get_sentences_list_matches(text, keysentence):
    """
    Check which key-sentences from occurs within a string
    and return the list of matches.

    :param text: text
    :type text: str or unicode
    :type: list(str or uniocde)
    :return: Set of sentences
    :rtype: set(str or unicode)
    """
    match = []
    text_list= text.split()
    for sentence in keysentence:
        if len(sentence.split()) > 1:
            if sentence in text:
                count = text.count(sentence)
                for i in range(0, count):
                    match.append(sentence)
        else:
            pattern = re.compile(r'^%s$'%sentence)
            for word in text_list:
                if re.search(pattern, word):
                    match.append(sentence)
    return sorted(match)


def preprocess_clean_page_spacy(clean_page,
                          preprocess_type=PreprocessWordType.LEMMATIZE):


    clean_list = clean_page.split(' ')
    page_string = ''
    for word in clean_list:
        preprocessed_word = query_utils.preprocess_word(word,
                                                         preprocess_type)
        if page_string == '':
            page_string = preprocessed_word
        else:
            page_string += (' ' + preprocessed_word)
    return page_string


def preprocess_clean_page_spacy(clean_page):
    nlp = spacy.load('en')
    doc = nlp(clean_page)
    page_nlp_spacy=[]
    for i, word in enumerate(doc):
        word_normalized=re.sub(NON_AZ_REGEXP, '', word.text.lower())
        output="%d\t%s\t%s\t%s\t%s\t%s\t%s\t"%( i+1, word, word_normalized, word.lemma_, word.pos_, word.tag_, word.ent_type_)
        page_nlp_spacy.append(output)
    return page_nlp_spacy


def georesolve_page_2(text, lang_model):
    nlp = spacy.load(lang_model)
    doc = nlp(text)
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml)
            dResolved_loc= coord_xml(geo_xml)
            return dResolved_loc
        else:
           return {}
    else:
        return {}

def georesolve_page(doc):
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geo_xml=georesolve_cmd(in_xml)
            dResolved_loc= coord_xml(geo_xml)
            print(dResolved_loc)
            return dResolved_loc
        else:
           return {}
    else:
        return {}

def geoparser_page(text):
    geo_xml=geoparser_cmd(text)
    dResolved_loc= geoparser_coord_xml(geo_xml)
    return dResolved_loc



def geomap_page(doc):
    geomap_html = ''
    if doc.ents:
        flag,in_xml = xml_geo_entities(doc)
        if flag == 1:
            geomap_html=geomap_cmd(in_xml)
    #return str(geomap_html)
    return geomap_html


def get_articles_nls(text):
    text_list= text.split()
    terms_view=[s.isupper() for s in text_list]
    articles_page={}
    key='previous_page'
    half_key=''
    cont = 0
    for i in range(0, len(terms_view)):
        if terms_view[i]== True:
            if ',' not in text_list[i]:
                half_key=half_key+text_list[i]
                
            else:
                if half_key!='':
                    key=half_key + text_list[i]
                    half_key=''
                else:
                    key=text_list[i]
                if key in articles_page:
                     cont = cont +1 
                     key=key+"-"+cont
                 
            articles_page[key] = ''
        else:
            if articles_page[key] != '' :
                articles_page[key]= articles_page[key] + ' ' + text_list[i]
            else:
                articles_page[key]= text_list[i]
    return articles_page

