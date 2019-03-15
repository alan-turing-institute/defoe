# Count number of articles containing two or more keywords and group by year

* For each article:
  - Look for the keywords provided by the user and form a list of all the keywords that occur in the article.
  - Record this list along with the article's year.
  - Use the lists of keywords to count the articles that share those lists of keywords.
  - Group the counts by year.
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
- count: <COUNT>
  words: [<WORD>, <WORD>, ...]
- ...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.txt`:

```
1907:
- count: 1
  words: [he, himself, his, it, king, them, they]
- count: 1
  words: [him, it, mr]
- count: 1
  words: [duke, his, mr]
- count: 1
  words: [her, husband, woman]
- count: 1
  words: [george, her, his, it,...
...
- count: 1
  words: [he, mr]
1915:
- count: 1
  words: [girl, him, man]
- count: 1
  words: [alexander, alice, boy, edward, george, girl,...
...
- count: 1
  words: [he, her, his, it, john]
```
