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

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/emigration_societies.txt`:

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
