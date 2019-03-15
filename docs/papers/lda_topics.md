# Get the Latent Dirochelet Allocation (LDA) topics for words within articles

* Both keyword and words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.lda_topics`
* Configuration file:
  - An LDA configuration file, in YAML format:

    ```        
    keyword: <KEYWORD>
    optimizer: online|em
    max_iterations: <N>
    ntopics: <N>
    topic_words: <N>
    ```

  - `<N>` must be >= 1 for each parameter.
  - Examples:
    - `queries/lda.yml`

* Result format:

```
<0>: [<WORD_0>, ..., <WORD_topicwords>]
<1>: [<WORD_0>, ..., <WORD_topicwords>]
<2>: [<WORD_0>, ..., <WORD_topicwords>]
...        
<ntopics>: [<WORD_0>, ..., <WORD_topicwords>]
years:[<MIN_YEAR>, <MAX_YEAR>]
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml`:

```
'0': ['', london, may, york, light]
'1': ['', new, princess, west, mines]
'2': ['', gold, deep, lft, ft]
'3': [new, '', liverpool, bombay, york]
'4': [co, princess, general, agents, '']
years: [1907, 1915]
```
