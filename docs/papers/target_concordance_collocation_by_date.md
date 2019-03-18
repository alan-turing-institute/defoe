# Get concordance and collocation for keywords occurring in articles which have a target word and group results by date

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
- [<WORD>, <CONCORDANCE>]
- [<WORD>, <CONCORDANCE>]
...
<YEAR>:
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/ladyqueenprincess.yml`:

```
1907:
- - lady
  - [f, ou, r, hawk, ll, ner, r, servant, elderly, for, lady, and, jv, ajfsfpsjr,
    vk, q, u, iet, coicfortable, home, applv]
- - lady
  - [beauty, of, scotland, the, scottish, switzerland, sir, walter, scott, '',
lady,
    of, the, lake, country, each, purple, peak, each, flinty, spire]
...
1915:
...
- - lady
  - [the, novelist, eat, in, the, stall, next, to, a, charming, lady, of, middle,
    age, she, said, at, the, end, of, the]
- - lady
  - [spiritless, he, doesnt, make, use, of, his, op, portunities, the, lady, frowned,
    he, wont, put, any, more, spirit, in, it, while]
```

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.yml`:

```
1907:
- - alexander
  - [being, given, director, john, brown, of, redliall, kincardineshire, pish,
salesman,
    alexander, craig, fish, merchant, poynernook, road, aberdeen, david, l, crombie,
    marwger]
- - alexander
  - [at, '', forfar, road, dun, dee, belonging, to, mr, jas, alexander, inelud, '',
    cow, pattly, in, full, milk, prime, fat, '']
...
1915:
...
- - it
  - [not, know, what, a, war, bonus, wa, the, claimant, thought, it, wa, a, gift,
    and, it, amount, depended, 'on', the, number]
- - it
  - [bonus, wa, the, claimant, thought, it, wa, a, gift, and, it, amount, depended,
    'on', the, number, of, shift, he, worked, being]
- - it
  - [bonus, which, depended, 'on', exactly, the, same, condition, a, wage, it, wa,
    clearly, part, of, claimant, wage]
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml` with `queries/emigration_taxonomy.yml`:

```
1901:
- - emigration
  - [the, cork, park, race, form, enter, taining, reading, '', the, emigration, of,
    woman, is, the, title, of, an, able, and, instruc]
- - emigration
  - [hii, '', answer, to, mr, chamberla, '', is, a, counter, emigration, '', c, '',
    c, signed, to, flood, south, a, '']
...
- - suitable
  - [facility, especially, light, railway, road, should, also, be, made, more, suitable,
    for, motor, traffic, and, pier, should, be, improved, there, wa]
1926:
- - colony
  - [mozambique, coast, bri, t, sii, east, africa, t, ttti, kenya, colony, lin, e,
    '', i, wffiisve, for, further, information, apply, fflce]
- - emigration
  - [of, every, description, all, at, inex, pensive, price, our, special, emigration,
    trunk, guaranteed, '', ply, birch, foundation, covered, brown, waterproof, canvas]
...
- - teacher
  - [men, teacher, had, increased, by, '', to, '', while, woman, teacher, had, in,
    creased, by, '', to, '', there, wa, a]
- - emigration
  - [taken, five, year, ago, it, had, dropped, to, '', besides, emigration, of, individual,
    and, of, family, from, dundee, ha, been, and]
```
