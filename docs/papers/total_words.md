# Count total number of words

* Query module: `defoe.papers.queries.total_words`
* Configuration file: None
* Result format:

```
{num_issues: <NUM_ISSUES>, num_words: <NUM_WORDS>}
```

* Validation:
  - The number of issues should be equal to the number of XML files over which the query was run.
  - The number of words should be equal to the number of `<wd>` elements in each XML file. This can be validated as follows, for example:


```bash
grep \<wd *xml | wc -l
```
```
132566
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml`:

```
{num_issues: 2, num_words: 132566}
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml`:

```
{num_issues: 7890, num_words: 482451795}
```
