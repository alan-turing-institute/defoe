# Get concordance and collocation for keywords occurring in articles which have a target word and groups the results by date

* Both keywords and words in documents are normalized, by removing all non-'a-z|A-Z' characters. They are then lemmatized - a lexical knowledge base is used to get the correct base form of each word (e.g. the base form of "ran" is "run"). Lemmatization is done using the NLTK [WordNet Lemmatizer](https://www.nltk.org/api/nltk.stem.html#module-nltk.stem.wordnet).
* The concordance includes the matching word plus 5 words either side.
* Query module: `defoe.papers.queries.target_concordance_collcation_by_date`
* Configuration file:
  - A target word and one or more words to search for, one per line.
  - Examples:
    - `queries/gender.txt`
    - `queries/ladyqueenprincess.txt`
    - `queries/emigration_taxonomy.txt`
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

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/ladyprincessqueen.txt`:

```
1907:
- - lady
  - [ner, r, servant, elderly, for, lady, and, jv, ajfsfpsjr, vk, q]
- - lady
  - [switzerland, sir, walter, scott, '', lady, of, the, lake, country, each]
- - lady
  - [specially, de, signed, for, stout, lady, highclass, corset, to, suit, all]
- - lady
  - [mewen, '', co, specialist, in, lady, dress, department, specialized, jighestclass,
...
1915:
...
- - lady
  - [my, friend, referring, to, two, lady, in, court, are, here, but]
- - lady
  - [stall, next, to, a, charming, lady, of, middle, age, she, said]
- - lady
  - [of, his, op, portunities, the, lady, frowned, he, wont, put, any]
```

Query over `0000164- The Courier and Argus/0000164_19070603.xml` and `0000164- The Courier and Argus/0000164_19151123.xml` with `queries/gender.txt`:

```


1907:
- - alexander
  - [of, redliall, kincardineshire, pish, salesman, alexander, craig, fish, merchant,
    poynernook, road]
- - alexander
  - [dee, belonging, to, mr, jas, alexander, inelud, '', cow, pattly, in]
...
1915:
...
- - it
  - [bonus, wa, the, claimant, thought, it, wa, a, gift, and, it]
- - it
  - [it, wa, a, gift, and, it, amount, depended, 'on', the, number]
- - it
  - [the, same, condition, a, wage, it, wa, clearly, part, of, claimant]
```

Query over all British Library Newspapers with `queries/emigration_taxonomy.txt`:

```
1763:
- - colony
  - [the, in, habitant, of, this, colony, inferted, in, the, ivth, article]
- - colony
  - [treaty, '', and, the, portuguefe, colony, which, may, have, been, conquered]
- - emigration
  - [ie, term, limited, for, this, emigration, fhall, be, nxeu, to, the]
- - emigration
  - [without, being, retrained, in, then, emigration, under, any, pretence, whatsoever,
    except]
...
1950:
- - emigration
  - [from, our, file, of, '', emigration, of, the, middle, class, we]
- - emigration
  - [our, population, by, whole, sale, emigration, there, is, rfcally, little, alternative]
- - service
  - [the, use, of, the, fighting, service, we, do, have, however, some]
```
