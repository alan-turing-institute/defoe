# Get colocates and group by year

* Both colocated words and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.alto.queries.colocates_by_year`
* Configuration file:
  - YAML file of form:

    ```
    start_word: <WORD>
    end_word: <WORD>
    window: <WINDOW>
    ```

  - `<WINDOW>` is the maximum number of intervening words and, if
    provided, must be >= 0. If omitted, a default of 0 is used.
  - Examples:
    - `queries/stranger_danger.yml`
* Result format:

```
<YEAR>:
- document_id: <DOCUMENT_ID>
  place: <PLACE>
  publisher: <PUBLISHER>
  filename: <FILENAME>
  matches:
  - start_page: <PAGE_ID>
    end_page: <PAGE_ID>
    span: [<WORD>, ..., <WORD>]
  - ...
  ...
<YEAR>:
...
```

## Sample results

Query over British Library Books `1510_1699/*.zip` with `queries/stranger_danger.yml`:

```
1640:
- document_id: '000241254'
  filename: .../1510_1699/000241254_0_1-90pgs__581128_dat.zip
  matches:
  - end_page: '000070'
    span: [stranger, loves, delight, and, sweetest, blisse, is, got, with, greatest,
      danger]
    start_page: '000070'
  place: London
  publisher: Richard Hodgkinson, for W. W. and Laurence Blaikelocke
  title: Poems ... viz. The Hermaphrodite. The Remedie of Love. Elegies. Sonnets,
    with other poems
1667:
- document_id: 002952721
  filename: .../1510_1699/002952721_0_1-346pgs__625035_dat.zip
  matches:
  - end_page: 000178
    span: [stranger, 'no', one, knew, his, face, liza, at, the, approach, of, danger]
    start_page: 000178
  place: London
  publisher: null
  title: 'Until the End: a story of real life'
```
