# Get context of specific words and group by word

* Get context (title, publisher, place, page, enclosing text, year) of each of a set of words and return, grouped by word. Words in the documents are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed before matches are done.
* Query module: `defoe.alto.queries.find_words_context_group_by_word`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<WORD>
- {page: <PAGE_NUMBER>,
   place: <PLACE>,
   publisher: <PUBLISHER>,
   text: <TEXT_WITHIN_WHICH_WORD_OCCURRED>,
   title: <TITLE>,
   year: <YEAR>}
- ...
<WORD>
...
```

## Sample results

Query over British Library Books `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
heart:
- {page: 000009,
   place: 'London]',
   publisher: null,
   text: '...',
   title: 'A Warning...',
   year: 1676}
- ...
```
