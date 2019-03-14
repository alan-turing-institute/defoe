# Count number of times that each keyword appears for every article that has a target word in it

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters. They are then lemmatized - a lexical knowledge base is used to get the correct base form of each word (e.g. the base form of "ran" is "run"). Lemmatization is done using the NLTK [WordNet Lemmatizer](https://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet).
* Query module: `defoe.papers.queries.target_and_keywords_count_by_year`
* Configuration file:
  - A target word and one or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/ladyqueenprincess.txt`
    - `queries/emigration_taxonomy.txt`
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

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/ladyprincessqueen.txt`:

```
1907:
- [princess, 2]
- [lady, 21]
- [queen, 3]
1915:
- [lady, 32]
```

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

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

Query over all British Library Newspapers with `queries/emigration_taxonomy.txt`:

```
1763:
- [empire, 2]
- [colony, 2]
- [emigration, 3]
1784:
- [emigration, 1]
- [maid, 1]
...
1950:
- [service, 1]
- [emigration, 2]
```
