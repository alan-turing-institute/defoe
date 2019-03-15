# Count number of occurrences of keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.keyword_by_year`
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

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.txt`:

```
1907:
- [man, 75]
- [mrs, 64]
- [alexander, 9]
- [agnes, 2]
- [jane, 2]
...
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/krakatoa.txt`:

```
1901:
- [krakatoa, 2]
1902:
- [krakatoa, 13]
1908:
- [krakatoa, 1]
1912:
- [krakatoa, 1]
1913:
- [krakatau, 1]
1916:
- [krakatau, 2]
1924:
- [krakatoa, 1]
```
