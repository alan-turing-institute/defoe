# Normalize

Count total number of documents, pages and words per year. This can be useful if wanting to see how the average number of documents, pages and words change over time.

* Query module: `defoe.alto.queries.normalize`
* Configuration file: None
* Result format:

```
<YEAR>: [<NUM_DOCUMENTS>, <NUM_PAGES>, <NUM_WORDS>]
...
```

## Sample results

Query over British Library Books `1510_1699/*.zip`:

```
null: [14, 1660, 366436]
1602: [1, 92, 14412]
1605: [3, 363, 82402]
1606: [3, 238, 54308]
1607: [4, 340, 82654]
1608: [1, 84, 20623]
1610: [3, 204, 39701]
1611: [2, 216, 53843]
1612: [2, 208, 50929]
...

1696: [20, 1516, 405974]
1697: [16, 1844, 725475]
1698: [10, 710, 229209]
...
```

Query over British Library Books `*/*.zip`:

```
null: [14, 1660, 366436]
1602: [1, 92, 14412]
1605: [3, 363, 82402]
1606: [3, 238, 54308]
1607: [4, 340, 82654]
1608: [1, 84, 20623]
1610: [3, 204, 39701]
1611: [2, 216, 53843]
1612: [2, 208, 50929]
1613: [1, 84, 20443]
...
1896: [1573, 506589, 138755318]
1897: [1638, 530816, 144777228]
1898: [1268, 420066, 123156558]
