# Count number of occurrences of keywords and group by word

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.alto.queries.keyword_by_word`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<WORD>:
- [<YEAR>, <NUM_WORDS>]
- ...
<WORD>:
...
```

