# Count number of articles containing both a target word and one or more keywords and group by year

* Query module: `defoe.papers.queries.target_and_keywords_by_year`
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
- count: <COUNT>
  target_word: <WORD>
  words: [<WORD>, <WORD>, ...]
- ...
...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/ladyqueenprincess.yml`:

```
1907:
- count: 1
  target_word: lady
  words: [princess]
- count: 2
  target_word: lady
  words: [queen]
```

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.yml`:

```
1907:
- count: 1
  target_word: he
  words: [charles, deer, him, his, it, itself, king, lord, man, mr, pig, them,
they]
- count: 1
  target_word: he
  words: [him, himself, his, it, man, mr, william]
...
- count: 1
  target_word: he
  words: [it, m, mr, they]
1915:
- count: 2
  target_word: he
  words: [his]

1915:
- count: 1
  target_word: he
  words: [brother, george, his, mr]
...
- count: 1
  target_word: he
  words: [her, his, it, itself, man, she, them, themselves, they]
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/emigration_taxonomy.yml`:

```
1901:
- count: 1
  target_word: emigration
  words: [bookkeeping, empire, engagement, governess, guardian, loan, maid, marriage,
    matron, mother, respectable, servant, service, success, suitable, teacher,training]
- count: 1
  target_word: emigration
  words: [colonial, colony, daughter, happiness, training]
...
1926:
- count: 1
  target_word: emigration
  words: [daughter, servant]
- count: 1
  target_word: emigration
  words: [colony, engagement, loan, maid, matron, mother, respectable, service, success,
    suitable]
```
