from __future__ import unicode_literals
import spacy
import sys 
from spacy import displacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag, tag
import spacy
import enum
from defoe import query_utils
from defoe.query_utils import PreprocessWordType
from nltk.corpus import words
from nltk.parse.util import taggedsent_to_conll
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


def get_page_idx(page, 
                 keywords,
                 preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets a list of keywords (and their indices) within an page.
    Page words are preprocessed. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: page
    :rtype page: defoe.papers.page.Page
    :return: sorted list of keywords and indices hat occur within page
    :rtype: list(str or unicode)
    """
    matches = set()
    for idx, word in enumerate(page.words):
        preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
        if preprocessed_word in keywords:
            match=(preprocessed_word, idx)
            matches.add(match)
    return page, sorted(list(matches))


def get_concordance(page, 
                    match, 
                    window,
                    preprocess_type=PreprocessWordType.NORMALIZE):
    """
    For a given keyword (and its position in an page), it returns the concordance of words (before and after) using a window.
    :param page: Page
    :type page: defoe.alto.page.Page
    :parm match: keyword and its position inside the page list
    :type: list
    :window: number of words to the right and left
    :type: integer
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: keyword and its concordance
    :rtype: list
    """
    keyword = match[0]
    idx = match[1]
    page_size= len(page.words)
     
    if idx >=window: 
        start_idx= idx-window
    else: 
        start_idx=0

    if idx + window >=page_size:
        end_idx = page_size
    else:
	end_idx= idx + window + 1
    
    prep_types =[]
    prep_t=["NORMALIZE", "STEM", "LEMMATIZE", "NONE"]
    for i in prep_t:
        concordance_words = []
        preprocess_type = PreprocessWordType[i]
        concordance_words.append("Preprocess Type: "+ str(preprocess_type))
        for word in page.words[start_idx:end_idx]:
	    concordance_words.append(query_utils.preprocess_word(word, preprocess_type))
        prep_types.append(concordance_words)
    return (keyword,prep_types)

def get_page_sentences(page, 
                 keywords,
                 preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Gets a list of keywords (and their indices) within an page.
    Page words are preprocessed. 
    :param page: Page
    :type page: defoe.alto.page.Page
    :param keywords: keywords
    :type keywords: list(str or unicode)
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: page
    :rtype page: defoe.papers.page.Page
    :return: sorted list of keywords and indices hat occur within page
    :rtype: list(str or unicode)
    """
    matches = set()
    page_string=""
    for word in page.words:
        page_string=page_string + " " + word
    page_sentences= query_utils.sentence_spliter(page_string)
    for sentence in page_sentences:
        try:
            sentence_token=query_utils.word_to_token(sentence)
            for token in sentence_token:
                preprocess_word=query_utils.preprocess_word(token,PreprocessWordType.NORMALIZE)
                if preprocess_word in keywords:
                    match=(preprocess_word, sentence)
                    matches.add(match)
        except:
            pass
    return page, sorted(list(matches))


def get_sentence_preprocessed(match, 
                    preprocess_type=PreprocessWordType.NORMALIZE):
    """
    For a given keyword (and its position in an page), it returns the concordance of words (before and after) using a window.
    :parm match: keyword and sentencet
    :type: list
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :return: keyword and its concordance
    :rtype: list
    """
    keyword = match[0]
    prep_types =[]
    preprocessed_words = []
    preprocessed_words.append("Preprocess Type: ORIGINAL STRING")
    preprocessed_words.append(match[1])
    prep_t=["NORMALIZE", "STEM", "LEMMATIZE"]
    #splits the sentence into tokens
    sentence_token=query_utils.word_to_token(match[1])
    prep_types.append(preprocessed_words)
    #applies 3 different preprocessing treatments (normalize,stem, lemmatize) to each token 
    for i in prep_t:
        preprocessed_words = []
        preprocess_type = PreprocessWordType[i]
        preprocessed_words.append("Preprocess Type: "+ str(preprocess_type))
        for word in sentence_token:
	    preprocessed_words.append(query_utils.preprocess_word(word, preprocess_type))
        prep_types.append(preprocessed_words)
    #labels each token with part-of-speach using the original string
    pos_tag=query_utils.part_of_speech(sentence_token) 
    pos_tokens = []
    pos_tokens.append("Preprocess Type: POS")
    for token in pos_tag:
       pos_tokens.append(token)
    prep_types.append(pos_tokens)
    #entity recognition using the part-of-speach list  
    er_tokens=[]
    er=query_utils.entity_recognition(pos_tag)
    er_tokens.append("Preprocess Type: ER")
    er_tokens.append(er)
    prep_types.append(er_tokens)
    
    return (keyword,prep_types)

def get_page_words(document,
                     preprocess_type=PreprocessWordType.NORMALIZE):
    """
    Get pages within a document and preprocessed them.
    For each page that includes, add a tuple of
    form:

        (<YEAR>, <DOCUMENT>, <PAGE>)


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
    for page in document:
        match = None
        for word in page.words:
            preprocessed_word = query_utils.preprocess_word(word, preprocess_type)
            match = (document.year, document, page, preprocessed_word)
            matches.append(match)
    return matches


def extract_sentences(document):
    """
    Gets the words  within an page, and returns the sentences without any type of preprocessing treatment to the words.
    :param page: Document
    :type page: defoe.alto.document
    :return: matches
    :rtype list: 
    :return: year and sentences 
    """
    matches = []
    page_string=""
    for page in document:
       for word in page.words:
          page_string=page_string + " " + word
       page_sentences= query_utils.sentence_spliter(page_string)
       for sentence in page_sentences:
          match = None
          match = (document.year, sentence)
          matches.append(match)
    return matches 


def get_page_text_preprocessed(raw_sentence, 
                    preprocess_type=PreprocessWordType.NORMALIZE):
    """
    For a given year and sentence (raw_sentence), it returns the sentence preprocessed 
    :parm raw_sentence: year and sentence
    :type: list
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :rtype: match: year, preprocessed sentence 
    """
   
    year= raw_sentence[0]
    sentence = raw_sentence[1]
    prep_types= []
    preprocessed_words = []
    preprocessed_words.append("Preprocess Type: ORIGINAL STRING")
    preprocessed_words.append(sentence)
    prep_t=["NORMALIZE", "STEM", "LEMMATIZE"]
    #splits the sentence into tokens
    sentence_token=query_utils.word_to_token(sentence)
    prep_types.append(preprocessed_words)
    #applies 3 different preprocessing treatments (normalize,stem, lemmatize) to each token 
    for i in prep_t:
        preprocessed_words = []
        preprocess_type = PreprocessWordType[i]
        preprocessed_words.append("Preprocess Type: "+ str(preprocess_type))
        for word in sentence_token:
	    preprocessed_words.append(query_utils.preprocess_word(word, preprocess_type))
        prep_types.append(preprocessed_words)
    #labels each token with part-of-speach using the original string
    pos_tag=query_utils.part_of_speech(sentence_token) 
    pos_tokens = []
    pos_tokens.append("Preprocess Type: POS")
    for token in pos_tag:
       pos_tokens.append(token)
    prep_types.append(pos_tokens)
    #entity recognition using the part-of-speach list  
    er_tokens=[]
    er=query_utils.entity_recognition(pos_tag)
    er_tokens.append("Preprocess Type: ER")
    er_tokens.append(er)
    prep_types.append(er_tokens)
    match=(year, prep_types)
    return match




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


def nltkConll(setence_text):
    """
    NLTK implementation
    Receives a sentences, and split them in tokens.
    Returning each token,normalized token,lemma, stem, POStag and NER  as an element in a list
    """
    output_total=[]
    doc=query_utils.word_to_token(setence_text)
    for i, word in enumerate(doc):
       word_normalized= query_utils.preprocess_word(word, PreprocessWordType.NORMALIZE)
       word_lema= query_utils.lemmatize(word_nornmalized)
       word_stem= query_utils.stem(word_normalized)
       pos_tag= list(tag.pos_tag([word])[0])[1]
       ner_tag= nltk.ne_chunk(tag.pos_tag([word]))
       output="%d\t%s\t%s\t%s\t%s\t%s\t%s\t"%( i+1, word, word_lemma, word_stem, pos_tag, ner_tag)
       output_total.append[output]
    return output_total


def spacyConll(sentence_text):
    """
    spaCy implementation
    Receives a sentences, and split them in tokens.
    Returning each token,normalized token,lemma, POS, tag and NER  as an element in a list
    """
    nlp = spacy.load('en')
    doc = nlp(sentence_text)
    output_total=[]
    for i, word in enumerate(doc):
        word_normalized= query_utils.preprocess_word(word, PreprocessWordType.NORMALIZE)
        output="%d\t%s\t%s\t%s\t%s\t%s\t%s"%( i+1, word, word_normalized, word.lemma_, word.tag_, word.ent_type)
        output_total.append(output)
    return output_total

def total_preprocessed(raw_sentence,
                    preprocess_type=PreprocessWordType.NORMALIZE):
    """
    For a given year and sentence (raw_sentence), it returns the sentence preprocessed 
    :parm raw_sentence: year and sentence
    :type: list
    :param preprocess_type: how words should be preprocessed
    (normalize, normalize and stem, normalize and lemmatize, none)
    :rtype: match: year, preprocessed sentence 
    """
    year = raw_sentence[0]
    sentence = raw_sentence[1]
    prep_types= []
    prep_types.append(nltkConll(sentence))
    #prep_types.append(spacyConll(sentence))
    match=(year, prep_types)
    return match

