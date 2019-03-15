# Finds every unique word and its frequency

* Words in documents are normalized, by removing all non-'a-z|A-Z' characters.
* Query module: `defoe.papers.queries.unique_words`
* Configuration file:
  - YAML file of form:

    ```
    threshold: <COUNT>
    ```

  - <COUNT> is >= 1 and the threshold beneath which words will not be included.
  - If no configuration file is provided then a threshold of 1 is assumed.
  - Examples:
    - `queries/unique_words.yml`
* Result format:

```
{
    <WORD>: <COUNT>,
    <WORD>: <COUNT>,
    ...
}
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml` with `queries/unique_words.yml`:

```
{? '' : 12874, a: 2414, aberdeen: 65, able: 47, about: 94, above: 26, ac: 13, accepted: 11,
  according: 13, account: 25, accused: 29, act: 31, action: 27, active: 12, acts: 11,
  ad: 22, added: 15, additional: 13, address: 17, adopted: 11, advance: 14, advanced: 12,
  africa: 24, african: 12, after: 107, afternoon: 32, afterwards: 12, again: 41, against: 71,
  age: 32, aged: 16, agents: 16, ago: 25, agreed: 23, ai: 11, aid: 14, air: 22, al: 15,
...
  wright: 12, written: 15, x: 49, y: 77, yards: 12, year: 78, years: 100, yesterday: 61,
  yet: 30, york: 52, you: 66, young: 67, your: 57}
```
