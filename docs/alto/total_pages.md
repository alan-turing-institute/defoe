# Count total number of pages

* Query module: `defoe.alto.queries.total_pages`
* Configuration file: None
* Result format:

```
{num_documents: <NUM_DOCUMENTS>, num_pages: <NUM_PAGES>}
```

* Validation:
  - The number of documents should be equal to the number of documents in the ZIP files over which the query was run. This can be checked by listing the contents of the ZIP files and counting the number of ALTO metadata file names. For example:

```bash
find . -name "*.zip*" -type f -exec unzip -l {} \; | grep meta | wc -l
```

  - The number of pages should be equal to the number of `<Page>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be validated as follows, for example:


```bash
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<Page ALTO/*xml | wc -l
```
```
42
```

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`: 

```
{num_documents: 2, num_pages: 42}
```

Query over British Library Books `1510_1699/*.zip`:

```
{num_documents: 693, num_pages: 62768}
```

Query over British Library Books `*/*.zip`:

```
{num_documents: 63701, num_pages: 22044324}
```
