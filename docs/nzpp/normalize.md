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
