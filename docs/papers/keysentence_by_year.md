# Count number of articles in which there are occurences of keysentences and groups them by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters. They are then lemmatized - a lexical knowledge base is used to get the correct base form of each word (e.g. the base form of "ran" is "run"). Lemmatization is done using the NLTK [WordNet Lemmatizer](https://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet).
* Query module: `defoe.papers.queries.target_and_keywords_count_by_year`
* Configuration file:
  - A target word and one or more words to search for, one per line.
  - Examples:
    - `queries/emigration_societies.txt`
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

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/ladyprincessqueen.txt`:


Query over all British Library Newspapers with `queries/emigration_societies.txt`:

```
1826:
- [emigration committee, 1]
1827:
- [emigration committee, 5]
1828:
- [emigration committee, 2]
- [emigration scheme, 1]
...
1949:
- [recruitment office, 2]
- [girl friendly society, 8]
1950:
- [girl friendly society, 9]
```
