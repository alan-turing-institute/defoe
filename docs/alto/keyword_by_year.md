# Count number of occurrences of keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.alto.queries.keyword_by_year`
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

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
1676:
- [heart, 4]
- [hearts, 1]
```

Query over British Library Books `1510_1699/*.zip` with `queries/diseases.txt`:

```
null:
- [consumption, 1]
1605:
- [consumption, 2]
1608:
- [consumption, 1]
1613:
- [consumption, 2]
1618:
- [cancer, 1]
1623:
- [consumption, 1]
1630:
- [consumption, 2]
1631:
- [consumption, 1]
1632:
- [consumption, 1]
1633:
- [whooping, 2]
- [consumption, 2]
1635:
- [consumption, 1]
1637:
- [consumption, 3]
1639:
- [whooping, 1]
1644:
- [cancer, 1]
1647:
- [consumption, 2]
1651:
- [cancer, 2]
- [consumption, 1]
1652:
- [consumption, 1]
- [cancer, 2]
1653:
- [consumption, 1]
1655:
- [cancer, 1]
1658:
- [consumption, 1]
- [cancer, 1]
1660:
- [whooping, 4]
1661:
- [whooping, 3]
1664:
- [whooping, 2]
- [consumption, 1]
- [measles, 1]
1667:
- [consumption, 2]
- [cancer, 1]
1668:
- [whooping, 1]
- [cancer, 1]
1670:
- [consumption, 1]
1671:
- [cancer, 2]
1672:
- [smallpox, 1]
- [consumption, 1]
1674:
- [consumption, 1]
1677:
- [cancer, 1]
1678:
- [cholera, 1]
- [whooping, 2]
1679:
- [whooping, 1]
- [smallpox, 1]
1681:
- [whooping, 1]
- [cancer, 1]
- [consumption, 1]
1682:
- [consumption, 1]
1684:
- [cancer, 3]
1686:
- [whooping, 2]
1687:
- [consumption, 1]
1688:
- [cancer, 3]
- [consumption, 1]
1689:
- [cancer, 2]
1690:
- [smallpox, 1]
- [consumption, 1]
1692:
- [smallpox, 1]
1693:
- [smallpox, 1]
1695:
- [cancer, 5]
- [consumption, 2]
1697:
- [smallpox, 1]
1698:
- [smallpox, 1]
```
