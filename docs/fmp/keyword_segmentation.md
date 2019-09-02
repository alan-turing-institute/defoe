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
- [1668, 1]
- [1689, 2]
- [1652, 2]
- [1688, 3]
- [1671, 2]
- [1658, 1]
- [1684, 3]
cholera:
- [1678, 1]
consumption:
- [1623, 1]
- [1613, 2]
- [1688, 1]
- [1637, 3]
- [1674, 1]
- [1653, 1]
- [1633, 2]
- [1695, 2]
- [1672, 1]
- [1647, 2]
- [1631, 1]
- [1635, 1]
- [1658, 1]
- [1605, 2]
- [1630, 2]
- [1681, 1]
- [1690, 1]
- [1667, 2]
- [1687, 1]
- [1682, 1]
- [null, 1]
- [1608, 1]
- [1670, 1]
- [1664, 1]
- [1632, 1]
- [1651, 1]
- [1652, 1]
measles:
- [1664, 1]
smallpox:
- [1693, 1]
- [1697, 1]
- [1698, 1]
- [1672, 1]
- [1679, 1]
- [1692, 1]
- [1690, 1]
whooping:
- [1678, 2]
- [1660, 4]
- [1633, 2]
- [1679, 1]
- [1661, 3]
- [1664, 2]
- [1639, 1]
- [1681, 1]
- [1686, 2]
- [1668, 1]
```
