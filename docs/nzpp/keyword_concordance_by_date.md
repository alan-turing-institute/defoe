# Get concordance for keywords and group by date

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.nzpp.queries.keyword_concordance_by_date`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
* Result format:

```
<DATE>:
- { 
    title: <TITLE>,
    paper_name: <NAME>,
    content: <PAGE_CONTENT>,
    word: <WORD>,
    filename: <FILENAME>
  }
...
<DATE>:
...
```

**Caution:** as this query returns each article's content, for every match, there is a risk that the query will fail due to lack of memory. This query should only be run with interesting words that are not expected to occur often.

## Sample results

Query over `1.xml` and `2.xml` with `queries/hearts.txt`:

```
1839-08-21:
- {content: 'HISTORICAL SKETCH OF THE COLONIZATION OF NEW ZEALAND... dauntless 
   heart 
   ...',
  filename: .../1.xml,
  paper_name: New Zealand Gazette and Wellington Spectator,
  title: 'HISTORICAL SKETCH
    OF THE COLONIZATION OF NEW ZEALAND. (New Zealand Gazette and Wellington Spectator,
    21 August 1839)',
  word: heart}
- {content: 'HISTORICAL SKETCH OF THE COLONIZATION OF NEW ZEALAND. (New Zealand Gazette
   ... hearts ...',
  filename: .../1.xml,
  paper_name: New Zealand Gazette and Wellington Spectator,
  title: 'HISTORICAL SKETCH
    OF THE COLONIZATION OF NEW ZEALAND. (New Zealand Gazette and Wellington Spectator,
    21 August 1839)',
  word: hearts}
```
