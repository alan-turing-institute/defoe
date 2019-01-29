# Total documents

* Count total number of documents.
* Query module: `defoe.alto.queries.total_documents`
* Configuration file: None
* Result format:

```
{documents: <NUM_DOCUMENTS>}
```

* Validation: the number of documents should be equal to the number of ZIP files over which the query was run.

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`:

```
{documents: 2}
```

Query over British Library Books `1510_1699/*.zip`:

```
{documents: 693}
```

Query over British Library Books `*/*.zip`:

```
{documents: 63701}
```
