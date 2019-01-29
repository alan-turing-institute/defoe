# Count specific words and group by year

* Count occurrences of each of a set of words and return counts, grouped by year. 
* Query module: `defoe.papers.queries.articles_containing_words`
* Configuration file: 
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
* Result format:

```
YEAR:
- [<WORD>, <NUM_WORDS>]
- [<WORD>, <NUM_WORDS>]
...
YEAR:
...
```

## Sample results

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

```
1907:
- [william, 10]
- [alice, 2]
- [jane, 1]
- [deer, 1]
- [itself, 4]
- [mr, 43]
...
```

Query over `0000164- The Courier and Argus/*.xml` with `queries/krakatoa.txt`:

```
1901:
- [krakatoa, 1]
1902:
- [krakatoa, 6]
1908:
- [krakatoa, 1]
1912:
- [krakatoa, 1]
1913:
- [krakatau, 1]
1916:
- [krakatau, 1]
1924:
- [krakatoa, 1]
```
