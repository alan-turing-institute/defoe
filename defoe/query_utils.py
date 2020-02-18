"""
Query-related utility functions and types.
"""

import os
import subprocess
import re
import enum
from lxml import etree
from nltk.stem import PorterStemmer, WordNetLemmatizer
import spacy
from spacy import displacy
import time
from spacy.tokens import Doc
from spacy.vocab import Vocab

NON_AZ_REGEXP = re.compile('[^a-z]')


class PreprocessWordType(enum.Enum):
    """
    Word preprocessing types.
    """
    NORMALIZE = 1
    """ Normalize word """
    STEM = 2
    """ Normalize and stem word """
    LEMMATIZE = 3
    """ Normalize and lemmatize word """
    NONE = 4
    """ Apply no preprocessing """


def parse_preprocess_word_type(type_str):
    """
    Parse a string into a PreprocessWordType.

    :param type_str: One of none|normalize|stem|lemmatize
    :type type_str: str or unicode
    :return: word preprocessing type
    :rtype: PreprocessingWordType
    :raises: ValueError if "preprocess" is not one of the expected
    values
    """
    try:
        preprocess_type = PreprocessWordType[type_str.upper()]
    except KeyError:
        raise KeyError("preprocess must be one of {} but is '{}'"
                       .format([k.lower() for k in list(
                           PreprocessWordType.__members__.keys())],
                               type_str))
    return preprocess_type


def extract_preprocess_word_type(config,
                                 default=PreprocessWordType.LEMMATIZE):
    """
    Extract PreprocessWordType from "preprocess" dictionary value in
    query configuration.

    :param config: config
    :type config: dict
    :param default: default value if "preprocess" is not found
    :type default: PreprocessingWordType
    :return: word preprocessing type
    :rtype: PreprocessingWordType
    :raises: ValueError if "preprocess" is not one of
    none|normalize|stem|lemmatize
    """
    if "preprocess" not in config:
        preprocess_type = default
    else:
        preprocess_type = parse_preprocess_word_type(config["preprocess"])
    return preprocess_type


def extract_data_file(config, default_path):
    """
    Extract data file path from "data" dictionary value in query
    configuration.

    :param config: config
    :type config: dict
    :param default_path: default path to prepend to data file path if
    data file path is a relative path
    :type default_path: str or unicode
    :return: file path
    :rtype: str or unicode
    :raises: KeyError if "data" is not in config
    """
    data_file = config["data"]
    if not os.path.isabs(data_file):
        data_file = os.path.join(default_path, data_file)
    return data_file


def extract_window_size(config, default=10):
    """
    Extract window size from "window" dictionary value in query
    configuration.

    :param config: config
    :type config: dict
    :param default: default value if "window" is not found
    :type default: int
    :return: window size
    :rtype: int
    :raises: ValueError if "window" is >= 1
    """
    if "window" not in config:
        window = default
    else:
        window = config["window"]
    if window < 1:
        raise ValueError('window must be at least 1')
    return window

def extract_years_filter(config):
    """
    Extract min and max years to filter data from "years_filter" dictionary value the query
    configuration. The years will be splited by the "-" character.
    
    years_filter: 1780-1918

    :param config: config
    :type config: dict
    :return: min_year, max_year
    :rtype: int, int
    """
    
    if "years_filter" not in config:
        raise ValueError('years_filter value not found in the config file')
    else:
        years= config["years_filter"]
        year_min=years.split("-")[0]
        year_max=years.split("-")[1]
    return year_min, year_max


def extract_output_path(config):
    """
    Extract output path from "output_path" dictionary value the query
    configuration. 
    
    output_path: /home/users/rfilguei2/LwM/defoe/OUTPUT/

    :param config: config
    :type config: dict
    :return: out_file
    :rtype: string
    """

    if "output_path" not in config:
        output_path="."
    else:
        output_path= config["output_path"]

    return output_path



def normalize(word):
    """
    Normalize a word by converting it to lower-case and removing all
    characters that are not 'a',...,'z'.

    :param word: Word to normalize
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    return re.sub(NON_AZ_REGEXP, '', word.lower())


def stem(word):
    """
    Reducing word to its word stem, base or root form (for example,
    books - book, looked - look). The main two algorithms are:

    - Porter stemming algorithm: removes common morphological and
      inflexional endings from words, used here
      (nltk.stem.PorterStemmer).
    - Lancaster stemming algorithm: a more aggressive stemming
      algorithm.

    Like lemmatization, stemming reduces inflectional forms to a
    common base form. As opposed to lemmatization, stemming simply
    chops off inflections.

    :param word: Word to stemm
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    stemmer = PorterStemmer()
    return stemmer.stem(word)


def lemmatize(word):
    """
    Lemmatize a word, using a lexical knowledge bases to get the
    correct base forms of a word.

    Like stemming, lemmatization reduces inflectional forms to a
    common base form. As opposed to stemming, lemmatization does not
    simply chop off inflections. Instead it uses lexical knowledge
    bases to get the correct base forms of words.

    :param word: Word to normalize
    :type word: str or unicode
    :return: normalized word
    :rtype word: str or unicode
    """
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)


def preprocess_word(word, preprocess_type=PreprocessWordType.NONE):
    """
    Preprocess a word by applying different treatments
    e.g. normalization, stemming, lemmatization.

    :param word: word
    :type word: string or unicode
    :param preprocess_type: normalize, normalize and stem, normalize
    and lemmatize, none (default)
    :type preprocess_type: defoe.query_utils.PreprocessWordType
    :return: preprocessed word
    :rtype: string or unicode
    """
    if preprocess_type == PreprocessWordType.NORMALIZE:
        normalized_word = normalize(word)
        preprocessed_word = normalized_word
    elif preprocess_type == PreprocessWordType.STEM:
        normalized_word = normalize(word)
        preprocessed_word = stem(normalized_word)
    elif preprocess_type == PreprocessWordType.LEMMATIZE:
        normalized_word = normalize(word)
        preprocessed_word = lemmatize(normalized_word)
    else:  # PreprocessWordType.NONE or unknown
        preprocessed_word = word
    return preprocessed_word

def longsfix_sentence(sentence):
    if "'" in sentence:
        sentence=sentence.replace("'", "\'\\\'\'")
    cmd = 'printf \'%s\' \''+ sentence + '\' | ./long_s_fix/lxtransduce -l spelling=./long_s_fix/f-to-s.lex ./long_s_fix/fix-spelling.gr'
    #cmd = 'echo " + sentence + " | ./long_s_fix/lxtransduce -l spelling=./long_s_fix/f-to-s.lex ./long_s_fix/fix-spelling.gr'
    proc=subprocess.Popen(cmd.encode('utf-8'), shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if "Error" in str(stderr):
        print("---Err: '{}'".format(stderr))
        stdout_value = sentence
    else:
        stdout_value = stdout

    proc.terminate()
    fix_s= stdout_value.decode('utf-8').split('\n')[0]
    if re.search('[aeiou]fs', fix_s):
        fix_final=re.sub('fs', 'ss', fix_s)
    else:
        fix_final = fix_s
    return fix_final

def spacy_nlp(text, lang_model):
   nlp = spacy.load(lang_model)
   doc = nlp(text)
   return doc

def serialize_doc(doc):
   nlp = spacy.load('en')
   vocab_bytes = nlp.vocab.to_bytes()
   doc_bytes = doc.to_bytes()
   return doc_bytes, vocab_bytes


def serialize_spacy(text):
    doc = spacy_nlp(text)
    doc_bytes, vocab_bytes = serialize_doc(doc)
    return [doc_bytes, vocab_bytes]


def deserialize_doc(serialized_bytes):
    vocab = Vocab()
    doc_bytes = serialized_bytes[0]
    vocab_bytes= serialized_bytes[1]
    vocab.from_bytes(vocab_bytes)
    doc = Doc(vocab).from_bytes(doc_bytes)
    return doc

def display_spacy(doc):
    disp_ent=''
    if doc.ents:
        disp_ent=displacy.render(doc, style="ent")
    return disp_ent
   
def spacy_entities(doc):
    output_total=[]
    entities=[(i, i.label_, i.label) for i in doc.ents]
    return entities

def xml_geo_entities(doc):
    id=0
    xml_doc='<placenames> '
    flag=0
    for ent in doc.ents:
       if ent.label_ == "LOC" or ent.label_ == "GPE":
            id=id+1
            toponym = ent.text
            child ='<placename id="' + str(id) + '" name="' + toponym + '"/> '
            xml_doc= xml_doc+child
            flag=1
    xml_doc=xml_doc+ '</placenames>'
    return flag, xml_doc

def georesolve_cmd(in_xml):
    georesolve_xml =''
    atempt=0
    flag = 1
    if "'" in in_xml:
        in_xml=in_xml.replace("'", "\'\\\'\'")
    #cmd = 'printf \'%s\' \''+ in_xml + ' \' | ./georesolve/scripts/geoground -g unlock -lb -8.6500, 54.6330, -0.7321, 60.8547. 2 -top '
    cmd = 'printf \'%s\' \''+ in_xml + '\' | ./georesolve/scripts/geoground -g unlockgeonames -top'
    while (len(georesolve_xml) < 5) and (atempt < 500) and (flag == 1): 
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        proc.terminate()
        atempt= atempt + 1
        stdout, stderr = proc.communicate()
        if "Error" in str(stderr):
            flag = 0
            print("err: '{}'".format(stderr))
            georesolve_xml = ''
        else:
            georesolve_xml = stdout
    return georesolve_xml


def coord_xml(geo_xml):
    dResolvedLocs = {}
    try:
        root = etree.fromstring(geo_xml)
        for child in root:
            toponymName = child.attrib["name"]
            toponymId = child.attrib["id"]
            for subchild in child:
                latitude = subchild.attrib["lat"]
                longitude = subchild.attrib["long"]
                dResolvedLocs[toponymName+"-"+toponymId] = (latitude, longitude)
    except:
        dResolvedLocs["cmd"]=geo_xml
    return dResolvedLocs

def geomap_cmd(in_xml):
    geomap_html = ''
    atempt=0
    if "'" in in_xml:
        in_xml=in_xml.replace("'", "\'\\\'\'")
    cmd = 'printf \'%s\' \''+ in_xml + ' \' | ./georesolve/scripts/geoground -g unlock -lb -8.6500, 54.6330, -0.7321, 60.8547. 2 -top | ./georesolve/bin/sys-i386-64/lxt -s ./georesolve/lib/georesolve/gazmap-leaflet.xsl'
    while (len(geomap_html) < 5) and (atempt < 500): 
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        proc.terminate()
        geomap_html = proc.communicate(timeout=100)[0]
        atempt= atempt + 1
    return geomap_html.decode("utf-8")


def geoparser_cmd(text):
    atempt=0
    flag = 1
    geoparser_xml = ''
    if "'" in text:
        text=text.replace("'", "\'\\\'\'")
    #cmd = 'echo \'%s\' \''+ text + ' \' | ./geoparser-v1.1/scripts/run -t plain -g unlock -lb -8.6500, 54.6330, -0.7321, 60.8547. 2 -top' 
    cmd = 'echo \'%s\' \''+ text + ' \' | ./geoparser-v1.1/scripts/run -t plain -g unlockgeonames -top' 
    while (len(geoparser_xml) < 5) and (atempt < 500) and (flag == 1): 
        proc=subprocess.Popen(cmd.encode('utf-8'), shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        proc.terminate()
        stdout, stderr = proc.communicate()
        if "Error" in str(stderr):
            flag = 0
            print("err: '{}'".format(stderr))
        else:
            geoparser_xml = stdout
    return geoparser_xml

def geoparser_coord_xml(geo_xml):
    dResolvedLocs = dict()
    try:
        root = etree.fromstring(geo_xml)
        for element in root.iter():
            if element.tag == "ent":
                if element.attrib["type"] == "location":
                    latitude = element.attrib["lat"]
                    longitude = element.attrib["long"]
                    toponymId = element.attrib["id"]
                    for subchild in element:
                        if subchild.tag == "parts":
                            for subsubchild in subchild:
                                toponymName = subsubchild.text
                                #print(toponymName, latitude, longitude)
                                dResolvedLocs[toponymName+"-"+toponymId] = (latitude, longitude)
    except:
        pass
    return dResolvedLocs

def geoparser_text_xml(geo_xml):
    text_ER=[]
    try:
        root = etree.fromstring(geo_xml)
        for element in root.iter():
            if element.tag == "text":
                for subchild in element:
                    if subchild.tag == "p":
                        for subsubchild in subchild:
                            for subsubsubchild in subsubchild:
                                if subsubsubchild.tag == "w":
                                    inf={}
                                    inf['p']= subsubsubchild.attrib["p"]
                                    inf['group'] = subsubsubchild.attrib["group"]
                                    inf['id'] = subsubsubchild.attrib["id"]
                                    inf['pws'] = subsubsubchild.attrib["pws"]
                                    if "locname" in subsubsubchild.attrib.keys():
                                        inf['locname'] = subsubsubchild.attrib["locname"]
                                    text_ER.append((subsubsubchild.text,inf))
                   

    except:
        pass
    return text_ER

def create_es_index(es_index, force_creation):
        """
        Create specified index if it doesn't already exist
        :param es_index: the name of the ES index
        :param force_creation: delete the original index and create a brand new index
        :return: bool created
        """
        created = False
        es_index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    settings.TITLE: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }},
                    settings.AUTHOR: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }},
                    settings.EDITION: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }},
                    settings.YEAR: {
                        "type": "text",
                        "fields": {
                            "date": {
                                "type": "date",
                                "format": "yyyy"
                            }
                        }
                    },
                    settings.PLACE: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.ARCHIVE_FILENAME: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.SOURCE_TEXT_FILENAME: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.TEXT_UNIT: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.TEXT_UNIT_ID: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.NUM_TEXT_UNIT: {
                        "type": "long",
                    },
                    settings.TYPE_ARCHIVE: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.MODEL: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.SOURCE_TEXT_CLEAN: {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    settings.NUM_WORDS: {
                        "type": "text",
                        "fields": {
                            "integer": {
                                "type": "integer"
                            }
                        }
                    },
                    settings.BOOK_ID: {
                        "type": "text",
                        "fields": {
                            "integer": {
                                "type": "integer"
                            }
                        }
                    },
                    "misc": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                }
            }
        }
        try:
            # Overwrite without checking if force param supplied
            if force_creation:
                # Explicitly delete in this case
                if Elasticsearch.get_instance().indices.exists(es_index):
                    Elasticsearch.get_instance().indices.delete(index=es_index)
                # Ignore 400 means to ignore "Index Already Exist" error.
                Elasticsearch.get_instance().indices.create(index=es_index, ignore=400, body=es_index_settings)
                # self.es.indices.create(index=es_index, ignore=400)
                created = True
            else:
                # Doesn't already exist so we can create it
                Elasticsearch.get_instance().indices.create(index=es_index, ignore=400, body=es_index_settings)
                created = True
        except Exception as ex:
            print('Error creating %s: %s' %(es_index, ex))
        finally:
            return created

