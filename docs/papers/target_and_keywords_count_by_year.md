# Count number of times that each keyword appears for every article that has a target word in it and group by year

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
    - `queries/emigration_taxonomy.yml`
    - `queries/gender.yml`
    - `queries/ladyqueenprincess.yml`
* Data file:
  - A target word followed by one or more words to search for, one per line.
  - Examples:
    - `queries/emigration_taxonomy.txt`
    - `queries/gender.txt`
    - `queries/ladyqueenprincess.txt`
* Result format:

```
<YEAR>:
- [<WORD>, <COUNT>]
- [<WORD>, <COUNT>]
...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/ladyqueenprincess.yml`:

```
1907:
- [princess, 2]
- [lady, 21]
- [queen, 3]
1915:
- [lady, 32]
```

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.yml`:

```
1907:
- [mr, 214]
- [man, 66]
...
- [robert, 13]
- [lad, 5]
1915:
- [her, 42]
- [sow, 2]
...
- [themselves, 4]
- [girl, 19]
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/emigration_taxonomy.yml`:

```
1901:
- [alien, 2]
- [bookkeeping, 23]
- [suitable, 166]
- [colonial, 16]
- [empire, 26]
...
- [colonial, 19]
- [daughter, 17]
1926:
- [matron, 2]
- [engagement, 1]
- [success, 1]
...
```
