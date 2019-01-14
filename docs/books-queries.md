# British Library Books dataset queries

## Total books

* Count total number of books.
* Query module: `lwm.books.queries.total_books`
* Configuration file: None
* Result format:

```
{books: <NUM_BOOKS>}
```

* Validation: the number of books should be equal to the number of ZIP files over which the query was run.

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`:

```
{books: 2}
```

Query over `1510_1699/*.zip`:

```
{books: 693}
```

Query over all books:

```
{books: 63701}
```

---

## Total pages

* Count total number of books and pages.
* Query module: `lwm.books.queries.total_pages`
* Configuration file: None
* Result format:

```
{books: <NUM_BOOKS>, pages: <NUM_PAGES>}
```

* Validation:
  - The number of books should be equal to the number of ZIP files over which the query was run.
  - The number of pages should be equal to the number of `<Page>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be val


```bash
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<Page ALTO/*xml | wc -l
```
```
42
```

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`: 

```
{books: 2, pages: 42}
```

Query over `1510_1699/*.zip`:

```
{books: 693, pages: 62768}
```

Query over all books: 

```
{books: 63701, pages: 22044324}
```

---

## Total words

* Count total number of books and words.
* Query module: `lwm.books.queries.total_words`
* Configuration file: None
* Result format:

```
{books: <NUM_BOOKS>, words: <NUM_WORDS>}
```

* Validation:
  - The number of words should be equal to the number of `<String>` elements in each XML file in the `ALTO` subdirectories within each zip file. This can be validated as follows, for example:

```bash
unzip 000000874_0_1-22pgs__570785_dat.zip
unzip 000001143_0_1-20pgs__560409_dat.zip
grep \<String ALTO/*xml | wc -l
```
```
4372
```

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip`:

```
{books: 2, words: 4372}
```

Query over `1510_1699/*.zip`:

```
{books: 693, words: 17479341}
```

Query over all books:

```
{books: 63701, words: 6866559285}
```

---

## Count specific words and group by year

* Count occurrences of each of a set of words and return counts, grouped by year. Words in the books are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed before matches are done.
* Query module: `lwm.books.queries.find_words_group_by_year`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<YEAR>
- [<WORD>, <NUM_WORDS>]
- [<WORD>, <NUM_WORDS>]
- ...
<YEAR>
...
```

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
1676:
- [hearts, 1]
- [heart, 4]
```

---

## Count specific words and group by word

* Count occurrences of each of a set of words and return counts per year, grouped by word. Words in the books are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed before matches are done.
* Query module: `lwm.books.queries.find_words_group_by_word`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<WORD>
- [<YEAR>, <NUM_WORDS>]
- [<YEAR>, <NUM_WORDS>]
- ...
<WORD>
...
```

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
heart:
- [1676, 4]
hearts:
- [1676, 1]
```

Query over `1510_1699/*.zip` with `queries/diseases.txt`:

```
cancer:
- [1655, 1]
- [1644, 1]
- [1681, 1]
- [1651, 2]
- [1677, 1]
- [1667, 1]
- [1618, 1]
- [1695, 5]
- [1689, 2]
- [1668, 1]
- [1652, 2]
- [1688, 3]
- [1671, 2]
- [1658, 1]
- [1684, 3]
cholera:
- [1678, 1]
consumption:
- [1630, 2]
- [1690, 1]
...
```

Query over all books with `query_args/diseases.txt`:

```
cancer:
- [1831, 26]
- [1799, 8]
- [1847, 77]
- [1655, 1]
- [1888, 99]
- [1792, 6]
- [1778, 2]
- [1746, 2]
- [1796, 2]
...
```

---

## Get context of specific words and group by year

* Get context (title, publisher, place, page, enclosing text) of each of a set of words and return, grouped by year. Words in the books are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed before matches are done.
* Query module: `lwm.books.queries.find_words_context_group_by_year`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/diseases.txt`
    - `queries/hearts.txt`
* Result format:

```
<YEAR>
- {page: <PAGE_NUMBER>,
   place: <PLACE>,
   publisher: <PUBLISHER>,
   text: <TEXT_WITHIN_WHICH_WORD_OCCURRED>,
   title: <TITLE>,
   word: <WORD>}
- ...
<YEAR>
...
```

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

```
1676:
- {page: 000009,
   place: 'London]',
   publisher: null,
   text: '...',
   title: 'A Warning...',
   word: heart}
- ...
```

---

## Get context of specific words and group by word

* Get context (title, publisher, place, page, enclosing text, year) of each of a set of words and return, grouped by word. Words in the books are converted to lower-case and non 'a-z' characters (e.g. commas, hyphens etc.) removed before matches are done.
* Query module: `lwm.books.queries.find_words_context_group_by_word`
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

### Sample results

Query over `1510_1699/000001143_0_1-20pgs__560409_dat.zip` and `1510_1699/000000874_0_1-22pgs__570785_dat.zip` with `queries/hearts.txt`:

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

---

## Normalize

* Count total number of books, pages and words. This can be useful if wanting to see how the average number of books, pages and words change over time.
* Query module: `lwm.books.queries.normalize`
* Configuration file: None
* Result format:

```
<YEAR>: [<NUM_BOOKS>, <NUM_PAGES>, <NUM_WORDS>]
<YEAR>: [<NUM_BOOKS>, <NUM_PAGES>, <NUM_WORDS>]
<YEAR>: [<NUM_BOOKS>, <NUM_PAGES>, <NUM_WORDS>]
...
```

### Sample results

Query over `1510_1699/*.zip`:

```
null: [14, 1660, 366436]
1602: [1, 92, 14412]
1605: [3, 363, 82402]
1606: [3, 238, 54308]
1607: [4, 340, 82654]
1608: [1, 84, 20623]
1610: [3, 204, 39701]
1611: [2, 216, 53843]
1612: [2, 208, 50929]
...

1696: [20, 1516, 405974]
1697: [16, 1844, 725475]
1698: [10, 710, 229209]
...
```

Query over all books:

```
null: [14, 1660, 366436]
1602: [1, 92, 14412]
1605: [3, 363, 82402]
1606: [3, 238, 54308]
1607: [4, 340, 82654]
1608: [1, 84, 20623]
1610: [3, 204, 39701]
1611: [2, 216, 53843]
1612: [2, 208, 50929]
1613: [1, 84, 20443]
...
1896: [1573, 506589, 138755318]
1897: [1638, 530816, 144777228]
1898: [1268, 420066, 123156558]
```
