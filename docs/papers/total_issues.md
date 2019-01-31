# Count total number of issues

* Query module: `defoe.papers.queries.total_issues`
* Configuration file: None
* Result format:

```
{num_issues: <NUM_ISSUES>}
```

* Validation: the number of issues should be equal to the number of XML documents over which the query was run.

## Sample results

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

```
{num_issues: 2}
```

Query over `0000164- The Courier and Argus/*.xml`:

```
{num_issues: 7890}
```
