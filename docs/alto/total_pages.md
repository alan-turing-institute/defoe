# Total pages

* Count total number of documents and pages.
* Query module: `defoe.alto.queries.total_pages`
* Configuration file: None
* Result format:

```
{documents: <NUM_DOCUMENTS>, pages: <NUM_PAGES>}
```

* Validation:
  - The number of documents should be equal to the number of ZIP files over which the query was run.
  - The number of pages should be equal to the number of `<Page>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be val


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
{documents: 2, pages: 42}
```

Query over British Library Books `1510_1699/*.zip`:

```
{documents: 693, pages: 62768}
```

Query over British Library Books `*/*.zip`:

```
{documents: 63701, pages: 22044324}
```
