# Count number of articles containing both a target word and one or more keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters. They are then lemmatized - a lexical knowledge base is used to get the correct base form of each word (e.g. the base form of "ran" is "run"). Lemmatization is done using the NLTK [WordNet Lemmatizer](https://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet).
* Query module: `defoe.papers.queries.target_and_keywords_by_year`
* Configuration file:
  - A target word and one or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/ladyqueenprincess.txt`
    - `queries/emigration_taxonomy.txt`
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

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/ladyprincessqueen.txt`:

```
1907:
- count: 1
  target_word: lady
  words: [princess]
- count: 2
  target_word: lady
  words: [queen]
```

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

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

Query over all British Library Newspapers with `queries/emigration_taxonomy.txt`:

```
1763:
- count: 1
  target_word: emigration
  words: [colony, empire]
1784:
- count: 1
  target_word: emigration
  words: [maid]
...
1950:
- count: 1
  target_word: emigration
  words: [service]
```
