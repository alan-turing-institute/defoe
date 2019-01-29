# Get articles containing specific words and group by year (XML)

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

## Sample results

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
