# Count total number of documents

* Query module: `defoe.alto.queries.total_documents`
* Configuration file: None
* Result format:

```
{num_documents: <NUM_DOCUMENTS>}
```

* Validation: the number of documents should be equal to the number of documents in the ZIP files over which the query was run. This can be checked by listing the contents of the ZIP files and counting the number of ALTO metadata file names. For example:

```bash
find . -name "*.zip*" -type f -exec unzip -l {} \; | grep meta | wc -l
```

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`:

```
{num_documents: 2}
```

Query over British Library Books `1510_1699/*.zip`:

```
{num_documents: 693}
```

Query over British Library Books `*/*.zip`:

```
{num_documents: 63701}
```
