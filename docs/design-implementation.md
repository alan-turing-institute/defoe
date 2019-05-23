# Design and implementation notes

## How defoe works

When running a query, a list of file names to run the query over needs to be provided by the user.

An [Apache Spark](https://spark.apache.org/) resilient distributed dataset (RDD) is created from these file names. The file names are partitioned and distributed across the processing nodes in the Spark cluster.

Each file is read and parsed into a set of Python objects, an object model, that represents the contents of the file. These objects are used by the Python code that implements each query.

The object model to use is specified by the user, depending upon the files they are querying. At present there are three object models:

* `books`: for British Library Books (BLB)
* `fmp`: for ALTO-compliant subset of Find My Past newspapers (FMP)
* `papers`: for British Library Newspapers (BLN) or Times Digital Archive (TDA)
* `generic_xml`: for arbitrary XML documents

BLB and the ALTO-compliant subset of FMP both conform to the [ALTO](https://www.loc.gov/standards/alto/) format. An abstract object model, `alto`, which is a parent of both the `books` and `fmp` object models represents the commonality between these models.

The query selected by the user is also object model-specific:

* `defoe.alto.queries` package contains queries for `books` and `fmp`.
* `defoe.papers.queries` package contains queries for `papers`.
* `defoe.generic_xml.queries` package contains queries for `generic_xml`.

## `alto` abstract parent model

This is an abstract object model representing ALTO documents.

The list of files to run the query over is expected to be a list of ZIP files.

A ZIP file is expected to contain one or more documents in ALTO format:

* Each document has an associated XML metadata file.
* Each document has one or more associated XML page files, one per each page of the document. Each of these page files are listed in the metadata file.

An `Archive` object reads a ZIP file. It checks the ZIP file contents and, using pattern matching, extracts the file names for metadata files and page files and caches these indexed by by document and page IDs.

When asked for a specific document, the `Archive` creates a new `Document` object. This is done for every request, no caching is done.

The `Document` object reads a metadata file for a specific document from the archive and extracts information about the document: code, title, publisher, place, years, page codes, and number of pages.

When asked for a specific page, the `Document` creates a new `Page` object. This is done for every request, no caching is done.

The `Page` object reads a page file from the archive and extracts information about the page: code, width, height. The `Page` object also caches the raw XML as a collection of Python [lxml](https://lxml.de/) objects.

When asked for its words, the `Page` retrieves these on-demand by running an XPath query over the cached XML objects. This is done for every request.

## `books` model: child of `alto` (BLB)

A ZIP file contains one or more books in ALTO format:

* Each book has an XML metadata file.
* Each book has one or more XML page files, one for each page of the book.

The ZIP archive is assumed to hold the following files and directories:

```
<METADATA_CODE>_metadata.xml
<METADATA_CODE>_metadata.xml
...
ALTO/
    <METADATA_CODE>_<FILE_CODE>.xml
    <METADATA_CODE>_<FILE_CODE>.xml
    ...
    <METADATA_CODE>_<FILE_CODE>.xml
    <METADATA_CODE>_<FILE_CODE>.xml
    ...
```

where:

* `<METADATA_CODE>` is `[0-9]*
* `<FILE_CODE>` is `[0-9_]*`

For example `000000874_0_1-22pgs__570785_dat.zip` holds:

```
000001143_metadata.xml
ALTO/
    000001143_000001.xml
    000001143_000002.xml
    000001143_000003.xml
    ...
    000001143_000020.xml
```

An `Archive` object subclassed from `alto.archive.Archive` provides the patterns for the metadata file names and page file names.

All other aspects of this object model are as for `alto`.

BLB ZIP files may be grouped into directories, one per time period e.g. `1510_1699`, `1700_1799`, ..., `1890_1899`. The object model is agnostic to this.

## `fmp` model: child of `alto` (FMP)

A ZIP file contains one or more newspaper issues in ALTO format:

* Each newspaper issue has an XML metadata file.
* Each newspaper issue has one or more XML page files, one for each page of the newspaper.

A ZIP archive corresponds to a document and each file to a page.

The ZIP archive is assumed to hold the following files:

```
<METADATA_CODE>_mets.xml
<METADATA_CODE>_<FILE_CODE>.xml
<METADATA_CODE>_<FILE_CODE>.xml
...
<METADATA_CODE>_mets.xml
<METADATA_CODE>_<FILE_CODE>.xml
<METADATA_CODE>_<FILE_CODE>.xml
...
```

where:

* `<METADATA_CODE>` is `[0-9]*?_[0-9]*?`
* `<FILE_CODE>` is `[0-9_]*`

For example 0318.zip holds:

```
0000239_18000318_mets.xml
0000239_18000318_0001.xml
0000239_18000318_0002.xml
0000239_18000318_0003.xml
0000239_18000318_0004.xml
```

An `Archive` object subclassed from `alto.archive.Archive` provides the patterns for the metadata file names and page file names.

All other aspects of this object model are as for `alto`.

## `papers` model (BLN/TDA)

The list of file to run the query over is expected to be a list of XML files.

Each XML file is expected to contain one issue of a newspaper:

* Each XML file is compliant with either:
  - LTO_issue.dtd schema (TDA)
  - ncco_issue.dtd schema (TDA)
  - GALENP.dtd schema (TDA)
  - bl_ncnp_issue_apex.dtd (BLN)
* Each XML file contains an `issue` element with one or more `article` elements, corresponding to articles.

An `Issue` object reads the XML file and extracts information about the issue: ID, date, page count, day of week. The `Issue` object also caches the raw XML as a collection of Python [lxml](https://lxml.de/) objects.

The `Issue` object also creates one `Article` object for each `article` element within the XML file.

The `Issue` object uses conditionals and XPath queries to pull out the ID, issue metadata, and articles. These allow for both the TDA and BLN XML Schema to be handled.

An `Article` object extracts from an `article` element information about the article: ID, title, OCR quality, page IDs. It also extracts any preamble and the words within the article. The `Article` object also caches its XML fragment as a collection of Python `lxml` objects

The `Article` object uses conditionals and pattern matching to pull out the page IDs. These allow for both the TDA and BLN XML Schema to be handled.

British Library Newspapers XML files may be grouped into directories, one per newspaper e.g. `0000164- The Courier and Argus`, `0000187- The Bath Chronicle` etc. The code is agnostic to this.

## `nzpp` model

The list of file to run the query over is expected to be a list of XML files.

Each XML file is expected to contain one issue of a newspaper:

* Each XML file is compliant with either:
  - GALENP.dtd schema (TDA)
  - bl_ncnp_issue_apex.dtd (BLN)
* Each XML file contains an `issue` element with one or more `article` elements, corresponding to articles.

An `Articles` object reads the XML file and extracts information about one or more articles within the XML file, and creates one `Article` object for each `result` element within the XML file.

An `Article` object extracts from an `article` element information about the article: title, date, enclosing newspaper name, article type and content. The `Article` object also caches its XML fragment as a collection of Python `lxml` objects.

## `generic_xml` model

The list of file to run the query over is expected to be a list of XML files.

Unlike in the other models, strict XML parsing, using [lxml.etree.XMLParser](https://lxml.de/api/lxml.etree.XMLParser-class.html), is used. XMLParser's `recover` option is disabled, meaning no attempt to parse broken XML is made,

## Limitations

The limitations of the code and the object model are as follows.

The user needs to specify, as a command-line parameter, the object model they ant the data to be parsed into.

There is no testing done to check whether the data is compliant with the object model. defoe takes it on trust that the files it is given can be parsed into the object model specified by the user. If the data and object model are not compliant unhandled errors may arise.

There is no testing for compliance to any file structure or XML Schema.

The query selected by the user is also object model-specific. Again, it is the user's responsibility to ensure that the query is consistent, and can work with, their chosen object model.

No caching of the RDDs is done. Every time a query is run the files are reread, and RDDs and objects are recreated.

No preprocessing of the text prior to running a query is done.

Normalization of words, to remove any non-`a-z|A-Z` characters (for both data and search terms provided by the user) is the responsibility of individual query implementations (a `defoe.query_utils.normalize` helper function is provided for this purpose).

For the `generic_xml` model:

* Namespace extraction is done solely on from the document's root element's `nsmap`. If namespaces are defined in sub-elements then there will be a need to traverse the XML e.g. by traversing elements using [Tree iteration](https://lxml.de/tutorial.html#tree-iteration).
* Shema locations are accessed from a root element as an attribute. An alternative is to run an XPath query e.g.

```
namespaces = {u'xsi': u"http://www.w3.org/2001/XMLSchema-instance"}
query = "//@xsi:schemaLocation"
result = document_tree.getroot().xpath(query, namespaces=namespaces)
result = [str(r) for r in result]
query = "//@xsi:noNamespaceSchemaLocation"
result = document_tree.getroot().xpath(query, namespaces=namespaces)
result = [str(r) for r in result]
```

## Notes

There are functions that could be reused in a preprocessing tool that, for example, parses raw XML, strips out stopwords, and stores both metadata and raw text.

Normalization of words could be done when XML files are parsed, rather than by the individual queries.

The `alto`, `books` and `fmp` models could be refactored to parse pages and extract text once, as done in `papers`, rather than on demand. The converse is also possible, with `papers` parsing files and `article` elements on demand.

The `papers` model could be refactored into a generic super-class with sub-classes for BLN and TDA. This would be cleaner, and more in the spirit of object-oriented design, than using conditionals and XPath queries to handle these differences within a single class.

The ALTO-compliant FMP subset of newspapers data is structured in a different way from the BLN/TDA newspapers data. The FMP subset consists of one XML file per page and one XML file per issue (the metadata file). This issue file also contains information on the articles in the issue. The content of the articles is spread across the XML pages. In contrast, the BLN/TDA data consists of one XML file per issue, with articles held as XML elements within each issue's file. A common super-class for FMP, BLN and TDA newspapers would require more than just different XPath queries. For example, to get article text from BLN/TDA requires pulling out content from the `article` element in a single issue file. In contrast, to get article text from FMP may require getting, from the metadata file for the issue, information on the pages, and so the files, which contain the article's text then parsing each of these in turn. This may be complicated by the fact that the page files don't seem to have any metadata specifically identifying articles. This may then incur having to searching the page text for the article title as recorded in the metadata file, and then searching for the title of the following article, to know when the end of the current article has been encountered.
