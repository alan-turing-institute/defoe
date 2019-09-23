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

