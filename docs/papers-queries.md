# British Library Newspapers dataset queries

## Count specific words and group by year

* Count occurrences of each of a set of words and return counts, grouped by year. 
* Query module: `defoe.papers.queries.articles_containing_words`
* Configuration file: 
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
* Result format:

```
YEAR:
- [<WORD>, <NUM_WORDS>]
- [<WORD>, <NUM_WORDS>]
...
YEAR:
...
```

### Sample results

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

```
1907:
- [william, 10]
- [alice, 2]
- [jane, 1]
- [deer, 1]
- [itself, 4]
- [mr, 43]
...
```

Query over `0000164- The Courier and Argus/*.xml` with `queries/krakatoa.txt`:

```
1901:
- [krakatoa, 1]
1902:
- [krakatoa, 6]
1908:
- [krakatoa, 1]
1912:
- [krakatoa, 1]
1913:
- [krakatau, 1]
1916:
- [krakatau, 1]
1924:
- [krakatoa, 1]
```

---

## Get articles containing specific words and group by year (XML)

* Get articles containing each of a set of words and return, grouped by year. Words in the books are converted to lower-case and non 'a-z' characters.
* Query module: `defoe.papers.queries.article_xml_with_words`
* Configuration file: 
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
* Result format:

```
YEAR 00:00:00: [<ARTICLE_XML>, <ARTICLE_XML>, ...]
YEAR 00:00:00: [<ARTICLE_XML>, <ARTICLE_XML>, ...]
...
```

### Sample results

Query over all newspapers with `queries/krakatoa.txt`:

```
1883-08-31 00:00:00: ["<article xmlns:dc=\"http://purl.org/dc/elements/1.1/\">
    ...
    <wd pos=\"2030,7775,2198,7806\">Krakatoa.</wd>
    ...
    </article>\n\t",
    "<article ...  </article>\n\t",
    ...],
1883-09-07 00:00:00: [...],
...
```

## Get articles containing specific words and group by year (plain-text)

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

### Sample results

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
