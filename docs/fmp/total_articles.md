# Count total number of articles

* Query module: `defoe.papers.queries.total_articles`
* Configuration file: None
* Result format:

```
{num_issues: <NUM_ISSUES>, num_articles: <NUM_ARTICLES>}
```

* Validation:
  - The number of issues should be equal to the number of XML files over which the query was run.
  - The number of articles should be equal to the number of `<article>` elements in each XML file. This can be validated as follows, for example:


```bash
grep \<article *xml | wc -l
```
```
287
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml`:

```
{num_articles: 287, num_issues: 2}
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml`:

```
{num_articles: 1024919, num_issues: 7890}
```
