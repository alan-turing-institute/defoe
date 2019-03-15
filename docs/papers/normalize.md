# Normalize

Count total number of issues, articles and words per year. This can be useful if wanting to see how the average number of issues, articles and words change over time.

* Query module: `defoe.papers.queries.normalize`
* Configuration file: None
* Result format:

```
<YEAR>: [<NUM_ISSUES>, <NUM_ARTICLES>, <NUM_WORDS>]
...
```

* Validation:
  - The number of issues for a year should be equal to the number of XML documents over which the query was run for that year. This can be validated as follows, for example, for XML documents in `0000164- The Courier and Argus`, published in 1901:

```
ls Part\ 1/0000164-\ The\ Courier\ and\ Argus/1901/*/*xml | wc -l
```
```
313
```

  - The number of articles should be equal to the number of `<article>` elements in each XML file. This can be validated as follows, for example, for XML documents in `0000164- The Courier and Argus`, published in 1901:

```
grep \<article Part\ 1/0000164-\ The\ Courier\ and\ Argus/1901/*/*xml | wc -l
```
```
41625
```

  - The number of words should be equal to the number of `<wd>` elements in each XML file. This can be validated as follows, for example, for XML documents in `0000164- The Courier and Argus`, published in 1901:

```
grep \<wd Part\ 1/0000164-\ The\ Courier\ and\ Argus/1901/*/*xml | wc -l
```
```
22502099
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml`:

```
1907: [1, 143, 70965]
1915: [1, 144, 61601]
```

Query over `Part 1/0000164- The Courier and Argus/*/*/*.xml`:

```
1901: [313, 41625, 22502099]
1902: [313, 39192, 22669151]
1903: [313, 38118, 22913623]
1904: [312, 41384, 24043707]
1905: [296, 39662, 21116077]
1906: [312, 42628, 21211564]
1907: [313, 40692, 21463718]
1908: [313, 42544, 21427434]
1909: [311, 46340, 20618648]
1910: [312, 45917, 20887133]
1911: [311, 45712, 19354700]
1912: [312, 45462, 20216866]
1913: [313, 49351, 20943916]
1914: [312, 42446, 18113848]
1915: [312, 38918, 16037381]
1916: [310, 35981, 14785921]
1917: [311, 24521, 11081492]
1918: [311, 18443, 8986091]
1919: [310, 30169, 14193708]
1920: [313, 31083, 15585838]
1921: [312, 40945, 16951926]
1922: [311, 44195, 18757498]
1923: [313, 48108, 20602701]
1924: [313, 46846, 21070029]
1925: [312, 47487, 20081958]
1926: [106, 17150, 6834768]
```
