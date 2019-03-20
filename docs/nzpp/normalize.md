# Normalize

Count total number of articles and words per year. This can be useful if wanting to see how the average number of articles and words change over time.

* Query module: `defoe.nzpp.queries.normalize`
* Configuration file: None
* Result format:

```
<YEAR>: [<NUM_ARTICLES>, <NUM_WORDS>]
...
```

## Sample results

Query over `1.xml` and `2.xml`:

```
1839: [32, 48587]
1840: [8, 5440]
```

Query over `*.xml`:

```
1839: [32, 48587]
1840: [988, 646558]
1841: [1277, 907515]
1842: [3234, 2522118]
1843: [4447, 3297503]
1844: [2865, 2211004]
1845: [3166, 2616238]
1846: [4898, 3471217]
1847: [6078, 4540781]
1848: [6852, 5181641]
1849: [6885, 5709136]
1850: [6786, 5930646]
1851: [7630, 6704759]
1852: [10847, 9801580]
1853: [10921, 9066243]
1854: [11539, 9752296]
1855: [10295, 7729710]
1856: [10660, 8229470]
1857: [15717, 12152039]
1858: [21182, 16602978]
1859: [22422, 18420647]
1860: [22709, 20466259]
1861: [25476, 22218661]
1862: [42194, 38963970]
1863: [9080, 7789281]
```
