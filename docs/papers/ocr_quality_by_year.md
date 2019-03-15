# Get measure of OCR quality for each article and group by year

* Query module: `defoe.papers.queries.ocr_quality_by_year`
* Configuration file: None
* Result format:

```
<YEAR>: [<QUALITY>, ...]
...
```

## Sample results

Query over `Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml` and `Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml`:

```
1907: [91.22, 85.82, 78.1, 76.0, 67.64, 75.34, 82.83, 75.49,
 75.87, 78.33, 82.74,...]
1915: [90.13, 80.48, 85.55, 82.36, 69.57, 82.06, 66.46, 74.6
, 83.75, 83.92, 82.47,...]
```
