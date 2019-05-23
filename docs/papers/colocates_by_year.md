# Get colocates and group by year

* Both colocated words and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.colocates_by_year`
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
- article_id: <ARTICLE_ID>
  issue_id: <ISSUE_ID>
  page_ids: <PAGE_IDS>
  filename: <FILENAME>
  matches:
  - [<WORD>, ..., <WORD>]
  - ...
- ...
...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/stranger_danger.yml`:

```
1907:
- article_id: 0000164_19070502_0003-032
  filename: .../Part 1/0000164- The Courier and Argus/1907/0000164_19070502/0000164_19070502.xml
  issue_id: 0000164_19070502
  matches:
  - [stranger, 'on', the, road, did, not, know, the, extent, of, the, danger]
  page_ids: ['0003']
  title: PERTHSHIRE NARROW ROADS.
1921:
- article_id: 0000164_19210530_0007-096
  filename: .../Part 1/0000164- The Courier and Argus/1921/0000164_19210530/0000164_19210530.xml
  issue_id: 0000164_19210530
  matches:
  - [stranger, to, you, and, i, heartily, thank, you, for, warning, me, of, my,
 danger]
  page_ids: ['0007']
  title: MADEMOISELLE OF MONTE CARLO
1925:
- article_id: 0000164_19251012_0005-127
  filename: .../Part 1/0000164- The Courier and Argus/1925/0000164_19251012/0000164_19251012.xml
  issue_id: 0000164_19251012
  matches:
  - [stranger, is, now, out, of, danger]
  page_ids: ['0005']
  title: LINLITHGOW VICTIM OUT OF DANGER.
```
