# Get concordance for keywords and group by word

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.alto.queries.keyword_concordance_by_word`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<WORD>:
- { title: <TITLE>,
    place: <PLACE>,
    publisher: <PUBLISHER>,
    page_number: <PAGE_NUMBER>,
    content: <PAGE_CONTENT>,
    year: <YEAR>,
    document_id: <DOCUMENT_ID>,
    filename: <FILENAME>}
- ...
<WORD>:
...
```

**Caution:** as this query returns each page's content, for every match, there is a risk that the query will fail due to lack of memory. This query should only be run with interesting words that are not expected to occur often.

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
heart:
- {page_number: 000009,
   place: 'London]',
   publisher: null,
   title: 'A Warning...'
   content: 'A WARNING...',
   year: 1676,
   document_id: 000000874,
   filename: .../1510_1699/000000874_0_1-22pgs__570785_dat.zip}
- {content: "unto him...",
   page_number: '000013',
   place: 'London]',
   publisher: null,
   title: 'A Warning...'
   year: 1676,
   document_id: 000000874,
   filename: .../1510_1699/000000874_0_1-22pgs__570785_dat.zip}
- ...
```
