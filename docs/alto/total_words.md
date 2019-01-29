# Total words

* Count total number of documents and words.
* Query module: `defoe.alto.queries.total_words`
* Configuration file: None
* Result format:

```
{documents: <NUM_DOCUMENTS>, words: <NUM_WORDS>}
```

* Validation:
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
{documents: 2, words: 4372}
```

Query over British Library Books `1510_1699/*.zip`:

```
{documents: 693, words: 17479341}
```

Query over British Library Books `*/*.zip`:

```
{documents: 63701, words: 6866559285}
```
