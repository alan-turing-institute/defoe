# Get concordance and collocation for keywords occurring in articles which have a target word and group results by date

* Query module: `defoe.papers.queries.target_concordance_collocation_by_date`
* Configuration file:
  - A configuration file in YAML format:

    ```
    preprocess: none|normalize|stem|lemmatize
    window: <WINDOW_SIZE>
    data: <DATA_FILE>
    ```

  - `none`: no word preprocessing is applied.
  - `normalize`: words are normalized by removing all non-'a-z|A-Z' characters.
  - `stem`: words are normalized then reduced to their word stems (for example, books - book, looked - look) using the Porter stemming algorithm which removes common morphological and inflexional endings from words. Stemming is done using the NLTK [Porter Stemmer](https://www.nltk.org//api/nltk.stem.html#module-nltk.stem.porter).
  - `lemmatize`: words are lemmatized using lexical knowledge bases to get the correct base forms of each word. Like stemming, lemmatization reduces inflectional forms to a common base form. As opposed to stemming, lemmatization does not simply chop off inflections. Instead it uses lexical knowledge bases to get the correct base forms of words. Lemmatization is done using the NLTK [WordNet Lemmatizer](https://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet).
  - If `preprocess` is ommitted then `lemmatize` is used.
  - `<WINDOW_SIZE>`: size of concordance returned.
  - If `window` is ommited then a window size of 10 is used.
  - `<DATA_FILE>`: path to a plain-text data file (see below). If this is a relative path then it is assumed to be relative to the directory in which the configuration file resides.

  - Examples:
    - `queries/emigration_taxonomy.yml`
    - `queries/gender.yml`
    - `queries/ladyqueenprincess.yml`
* Data file:
  - A target word followed by one or more words to search for, one per line.
  - Examples:
    - `queries/emigration_taxonomy.txt`
    - `queries/gender.txt`
    - `queries/ladyqueenprincess.txt`
* Result format:

```
<YEAR>:
- [<FILEMAME>, <WORD>, <CONCORDANCE>, <OCR>]
- [<FILEMAME>, <WORD>, <CONCORDANCE>, <OCR>]
...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/ladyqueenprincess.yml`:

```
1907:
- - .../Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml
  - lady
  - [f, ou, r, hawk, ll, ner, r, servant, elderly, for, lady, and, jv, ajfsfpsjr,
    vk, q, u, iet, coicfortable, home, applv]
  - 85.82
- - .../Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml
  - lady
  - [beauty, of, scotland, the, scottish, switzerland, sir, walter, scott, '', lady,
    of, the, lake, country, each, purple, peak, each, flinty, spire]
  - 85.82
...
1915:
...
- - .../Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml
  - lady
  - [f, rade, or, elderly, man, might, suit, able, i, crais, lady, bank, '', r,
'',
    li, l, '', fr, hawking, van]
  - 85.55
...
- - .../Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml
  - lady
  - [spiritless, he, doesnt, make, use, of, his, op, portunities, the, lady, frowned,
    he, wont, put, any, more, spirit, in, it, while]
  - 92.33
```

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.yml`:

```
1907:
- - .../Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml
  - alexander
  - [being, given, director, john, brown, of, redliall, kincardineshire, pish, salesman,
    alexander, craig, fish, merchant, poynernook, road, aberdeen, david, l, crombie,
    marwger]
  - 85.82
- - .../Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml
  - alexander
  - [at, '', forfar, road, dun, dee, belonging, to, mr, jas, alexander, inelud,
'',
    cow, pattly, in, full, milk, prime, fat, '']
  - 85.82
...
1915:
- - .../Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml
  - alexander
  - [november, '', notice, all, party, having, claim, against, the, late, alexander,
    ilay, farmer, newton, of, kirk, buddo, are, requested, to, lodge]
  - 85.55
...
- - .../Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml
  - it
  - [bonus, which, depended, 'on', exactly, the, same, condition, a, wage, it, wa,
    clearly, part, of, claimant, wage]
  - 93.26
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/emigration_taxonomy.yml`:

```
1901:
- - .../Part 1/0000164- The Courier and Argus/1901/0000164_19010328/0000164_19010328.xml
  - daughter
  - [wa, well, a, '', m, they, did, me, good, my, daughter, year, passed, but, the,
    unpleasant, x, '', w, '', had]
  - 77.3
- - .../Part 1/0000164- The Courier and Argus/1901/0000164_19010328/0000164_19010328.xml
  - emigration
  - [advice, given, a, '', to, suitability, op, snops, and, good, emigration, to,
    chillfare, reduced, to, '', s, for, arttracs, agriculturist, wih]
  - 77.3
...
1926:
- - .../Part 1/0000164- The Courier and Argus/1926/0000164_19260105/0000164_19260105.xml
  - emigration
  - [of, the, farmer, union, yesterday, in, regard, to, the, government, emigration,
    policy, public, money, is, devoted, to, subsidising, passage, to, canada]
  - 93.04
...
- - .../Part 1/0000164- The Courier and Argus/1926/0000164_19260120/0000164_19260120.xml
  - failure
  - [pro, posed, grant, of, '', to, assist, imperial, trade, the, failure, to, carry,
    into, operation, the, recommendation, of, the, scottish, agricul]
  - 92.81
```
