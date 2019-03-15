# Get concordance and collocation for keywords occurring in articles which have a target word and group results by date

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

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/gender.txt`:

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

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml`:

```
1901:
- - emigration
  - [enter, taining, reading, '', the, emigration, of, woman, is, the, title]
- - emigration
  - [chamberla, '', is, a, counter, emigration, '', c, '', c, signed]
...
1926:
- - emigration
  - [printed, form, of, contract, canadian, emigration, the, scheme, under, which,
    the]
- - emigration
  - [financial, assistance, to, secure, the, emigration, to, canada, of, farm, worker]
- - emigration
  - [rt, i, '', euro, pan, emigration, '', '', '', pro, '']
...
```
