# Count number of occurrences of keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.nls.queries.keyword_by_year`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<YEAR>:
- [<WORD>, <NUM_WORDS>]
- ...
<YEAR>:
...
```

