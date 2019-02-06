# Count number of articles containing two or more keywords and group by year

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.keywords_by_year`
* Configuration file:
  - One or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/krakatoa.txt`
    - `queries/prof.txt`
* Result format:

```
<YEAR>:
- {
    "words": "<WORD>, <WORD>, ...",
    "count": <COUNT>
  }
- {
    "words": "<WORD>, <WORD>, ...",
    "count": <COUNT>
  }
- ...
<YEAR>:
...
...
```

## Sample results

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

```
1907:
- {count: 1, words: '[''he'', ''himself'', ''his'', ''it'', ''king'', ''them'', ''they'']'}
- {count: 1, words: '[''him'', ''it'', ''mr'']'}
- {count: 1, words: '[''duke'', ''his'', ''mr'']'}
- {count: 1, words: '[''her'', ''husband'', ''woman'']'}
- {count: 1, words: '[''george'', ''her'', ''his'', ''it'',
...
- {count: 1, words: '[''he'', ''mr'']'}
1915:
- {count: 1, words: '[''girl'', ''him'', ''man'']'}
- {count: 1, words: '[''alexander'', ''alice'', ''boy'', ''edward'', ''george'', ''girl'',
...
- {count: 1, words: '[''he'', ''her'', ''his'', ''it'', ''john'']'}
```
