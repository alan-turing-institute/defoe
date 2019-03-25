# Get concordance for keywords and group by date

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.keyword_concordance_by_date`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
* Result format:

```
<DATE>:
- title: <TITLE>
  page_ids: <PAGE_IDS>
  content: <PAGE_CONTENT>
  word: <WORD>
  article_id: <ARTICLE_ID>
  issue_id: <ISSUE_ID>
  filename: <FILENAME>
...
<DATE>:
...
```

**Caution:** as this query returns each article's content, for every match, there is a risk that the query will fail due to lack of memory. This query should only be run with interesting words that are not expected to occur often.

## Sample results

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/krakatoa.txt`:

```
1901-01-02:
- article_id: 0000164_19010102_0005-063
  content: "THE EARTH...",
  filename: .../Part 1/0000164- The Courier and Argus/1901/0000164_19010102/0000164_19010102.xml
  issue_id: 0000164_19010102
  page_ids: ['0005']
  title: THE EARTH AND ITS HEAT
  word: krakatoa
1902-03-05:
- article_id: 0000164_19020305_0007-106
  content: "EARTHQUAKE TERRORS...",
  filename: .../Part 1/0000164- The Courier and Argus/1902/0000164_19020305/0000164_19020305.xml
  issue_id: 0000164_19020305
  page_ids: ['0007']
  title: EARTHQUAKE TERRORS.
  word: krakatoa
1902-05-14:
- article_id: 0000164_19020514_0007-110
  issue_id: 0000164_19020514
  ...
```
