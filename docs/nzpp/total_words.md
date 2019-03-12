# Count total number of words

* Query module: `defoe.nzpp.queries.total_words`
* Configuration file: None
* Result format:

```
{num_articles: <NUM_ARTICLES>, num_words: <NUM_WORDS>}
```

* Validation:
  - The number of articles should be equal to the number of `<result>` elements in each XML file. This can be validated as follows, for example:

```bash
grep \<result\> ~/data/nzpp/*xml | wc -l
```
```
40
```

## Sample results

Query over `1.xml` and `2.xml`:

```
{num_articles: 40, num_words: 54027}
```

Query over `*.xml`:

```
{num_articles: 268180, num_words: 224980837}
```
