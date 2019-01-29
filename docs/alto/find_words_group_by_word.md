# Count specific words and group by word

* Count occurrences of each of a set of words and return counts per year, grouped by word. Words in the documents are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed before matches are done.
* Query module: `defoe.alto.queries.find_words_group_by_word`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<WORD>
- [<YEAR>, <NUM_WORDS>]
- [<YEAR>, <NUM_WORDS>]
- ...
<WORD>
...
```

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
heart:
- [1676, 4]
hearts:
- [1676, 1]
```

Query over British Library Books `1510_1699/*.zip` with `queries/diseases.txt`:

```
cancer:
- [1655, 1]
- [1644, 1]
- [1681, 1]
- [1651, 2]
- [1677, 1]
- [1667, 1]
- [1618, 1]
- [1695, 5]
- [1689, 2]
- [1668, 1]
- [1652, 2]
- [1688, 3]
- [1671, 2]
- [1658, 1]
- [1684, 3]
cholera:
- [1678, 1]
consumption:
- [1630, 2]
- [1690, 1]
...
```

Query over British Library Books `*/*.zip` with `query_args/diseases.txt`:

```
cancer:
- [1831, 26]
- [1799, 8]
- [1847, 77]
- [1655, 1]
- [1888, 99]
- [1792, 6]
- [1778, 2]
- [1746, 2]
- [1796, 2]
...
```
