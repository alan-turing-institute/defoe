# Get concordance for keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.alto.queries.keyword_concordance_by_year`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<YEAR>:
- { title: <TITLE>,
    place: <PLACE>,
    publisher: <PUBLISHER>,
    page_number: <PAGE_NUMBER>,
    content: <PAGE_CONTENT>,
    word: <WORD>,
    document_id: <DOCUMENT_ID>,
    filename: <FILENAME>}
- ...
<YEAR>:
...
```

**Caution:** as this query returns each page's content, for every match, there is a risk that the query will fail due to lack of memory. This query should only be run with interesting words that are not expected to occur often.

