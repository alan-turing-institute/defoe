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

