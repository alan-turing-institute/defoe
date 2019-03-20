# Count total number of words

* Query module: `defoe.alto.queries.total_words`
* Configuration file: None
* Result format:

```
{num_documents: <NUM_DOCUMENTS>, num_words: <NUM_WORDS>}
```

* Validation:
  - The number of documents should be equal to the number of documents in the ZIP files over which the query was run. This can be checked by listing the contents of the ZIP files and counting the number of ALTO metadata file names. For example:

```bash
find . -name "*.zip" -type f -exec unzip -l {} \; | grep meta | wc -l
```

  - The number of words should be equal to the number of `<String>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be validated as follows, for example:

```bash
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<String ALTO/*xml | wc -l
```
```
4372
```

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`:

```
{num_documents: 2, num_words: 4372}
```

Query over British Library Books `1510_1699/*.zip`:

```
{num_documents: 693, num_words: 17479341}
```

Query over British Library Books `*/*.zip`:

```
{num_documents: 63701, num_words: 6866559285}
```
