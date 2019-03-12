# Counts number of articles containing both a target word and one or more keywords and groups by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.target_and_keywords_by_year`
* Configuration file:
  - A target word and one or more words to search for, one per line.
  - Examples:
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

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/ladyprincessqueen.txt`:

```
1907:
- count: 1
  target_word: lady
  words: [princess]
- count: 1
  target_word: lady
  words: [queen]
```

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

```
1907:
- count: 1
  target_word: he
  words: [mr]
- count: 1
  target_word: he
  words: [agnes, brother, her, him, husband, lord, man, she, woman]
...
- count: 2
  target_word: he
  words: [his, it]
1915:
- count: 1
  target_word: he
  words: [brother, george, his, mr]
...
- count: 1
  target_word: he
  words: [her, his, it, itself, man, she, them, themselves, they]
```
