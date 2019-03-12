# Get measure of OCR quality for each page and group by year

* Query module: `defoe.alto.queries.ocr_quality_by_year`
* Configuration file: None
* Result format:

```
<YEAR>: [<QUALITY>, ...]
...
```

**Note:** If no `PC` attribute is present in the `Page` elements of the XML being queried then `null` is returned for each page.
