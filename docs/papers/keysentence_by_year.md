# Count number of articles in which there are occurences of keysentences and groups them by year

* Query module: `defoe.papers.queries.target_and_keywords_count_by_year`
* Configuration file:
  - A configuration file in YAML format:

    ```  
    preprocess: none|normalize|stem|lemmatize
    data: <DATA_FILE>
    ```

  - `none`: no word preprocessing is applied.
  - `normalize`: words are normalized by removing all non-'a-z|A-Z' characters.
  - `stem`: words are normalized then reduced to their word stems (for example, books - book, looked - look) using the Porter stemming algorithm which removes common morphological and inflexional endings from words. Stemming is done using the NLTK [Porter Stemmer](https://www.nltk.org//api/nltk.stem.html#module-nltk.stem.porter).
  - `lemmatize`: words are lemmatized using lexical knowledge bases to get the correct base forms of each word. Like stemming, lemmatization reduces inflectional forms to a common base form. As opposed to stemming, lemmatization does not simply chop off inflections. Instead it uses lexical knowledge bases to get the correct base forms of words. Lemmatization is done using the NLTK [WordNet Lemmatizer](https://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet).
  - If `preprocess` is ommitted then `lemmatize` is used.
  - `<DATA_FILE>`: path to a plain-text data file (see below). If this is a relative path then it is assumed to be relative to the directory in which the configuration file resides.
  - Examples:
    - `queries/emigration_societies.yml`
* Data file:
  - A target word and one or more words to search for, one per line.
  - Examples:
    - `queries/emigration_societies.yml`
* Result format:

```
<YEAR>:
- [<SENTENCE>, <COUNT>]
- [<SENTENCE>, <COUNT>]
...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/emigration_societies.yml`:

```
1901:
- [emigration scheme, 2]
- [emigration agent, 2]
- [girl friendly society, 4]
- [emigrant information office, 2]
- [british woman emigration association, 2]
1902:
- [governess benevolent institution, 1]
- [emigration agent, 2]
- [british woman emigration association, 2]
- [girl friendly society, 10]
...
1925:
- [emigration agent, 3]
- [girl friendly society, 15]
- [emigration scheme, 1]
1926:
- [emigration scheme, 1]
- [girl friendly society, 5]
```
