# Count number of occurrences of keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.nzpp.queries.keyword_by_year`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
    - `queries/prof.txt`
* Result format:

```
<YEAR>:
- [<WORD>, <NUM_WORDS>]
- ...
<YEAR>:
...
```

## Sample results

Query over `1.xml` and `2.xml` with `queries/hearts.txt`:

```
1839:
- [heart, 2]
- [hearts, 1]
```

Query over `1.xml` and `2.xml` with `queries/gender.txt`:

```
1839:
- [mary, 1]
- [brother, 4]
- [king, 6]
- [philip, 15]
- [master, 7]
...
1840:
- [his, 8]
- [daniel, 1]
- [philip, 3]
...
```
