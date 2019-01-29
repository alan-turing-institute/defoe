# Get articles containing specific words and group by year (plain-text)

* Get articles containing each of a set of words and return, grouped by year. Words in the books are converted to lower-case and non 'a-z' characters.
* Query module: `defoe.papers.queries.articles_containing_words_context`
* Configuration file: 
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
* Result format:

```
YEAR:
- { "filename": FILENAME,
    "newspaper_id": NEWSPAPER_ID,
    "article_title": TITLE,
    "article_id": ARTICLE_ID,
    "page_ids": [PAGE_ID, PAGE_ID, ...],
    "text": TEXT }
- { ... }
  ...
YEAR:
...
```

## Sample results

Query over all newspapers with `queries/krakatoa.txt`:

```
1883-08-31:
- article_id: 0000237_18830831_0003-004
  article_title: ...
  filename: /.../blpaper/xmls/0000237- The Lincoln Rutland and Stamford
    Mercury/0000237_18830831.xml
  newspaper_id: ...
  page_ids: ['0003']
  text: ...
- article_id: 0000406_18830831_0002-014
  article_title: V...
  filename: /.../blpaper/xmls/0000406- The Western Gazette/0000406_18830831.xml
  newspaper_id: ...
  page_ids: ['0002']
  text: ...
...
```
