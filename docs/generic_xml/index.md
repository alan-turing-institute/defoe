# XML dataset queries

General:

* [Gets metadata about an XML document](#Gets-metadata-about-an-XML-document)
* [Gets metadata about an XML document and counts frequences of each type of metadata](#Gets-metadata-about-an-XML-document-and-counts-frequences-of-each-type-of-metadata)
* [Counts total number of documents](#Counts-total-number-of-documents)
* [Finds every unique document type and its frequency](#Finds-every-unique-document-type-and-its-frequency)
* [Finds every unique namespace and its frequency](#Finds-every-unique-namespace-and-its-frequency)
* [Finds every unique root element and its frequency](#Finds-every-unique-root-element-and-its-frequency)
* [Counts total size of document files in bytes](#Counts-total-size-of-document-files-in-bytes)

---

## Gets metadata about an XML document

* Query module: `defoe.generic_xml.queries.get_metadata`
* Configuration file: None
* Result format:

```
- <FILENAME>:
  doctype: <DOCTYPE>,
  namespaces: {<TAG>: <URL>, <TAG>: <URL>, ...},
  no_ns_schema_location: <URL> | None,
  root: <ROOT_ELEMENT>,
  schema_locations: [<URL>, <URL>, ...] | None,
  size: <FILE_SIZE>
- <FILENAME>: ...
...
```

---

## Gets metadata about an XML document and counts frequences of each type of metadata

* Query module: `defoe.generic_xml.queries.summarize_metadata`
* Configuration file: None
* Result format:

```
doc_type:
- <DOCTYPE>: <COUNT>
- ...
root:
- <ROOT_ELEMENT>: <COUNT>
- ...
namespace:
- <NAMESPACE>: <COUNT>
- ...
schemaLocationL
- <URL>: <COUNT>
noNsSchemaLocation
- <URL>: <COUNT>
- ...

```

---

## Counts total number of documents

* Query module: `defoe.generic_xml.queries.total_documents`
* Configuration file: None
* Result format:

```
num_documents: <NUM_DOCUMENTS>
```

---

## Finds every unique document type and its frequency

* Query module: `defoe.generic_xml.queries.doc_types`
* Configuration file: None
* Result format:

```
<DOCTYPE>: <COUNT>
<DOCTYPE>: <COUNT>
...
```

---

## Finds every unique namespace and its frequency

* Query module: `defoe.generic_xml.queries.namespaces`
* Configuration file: None
* Result format:

```
<NAMESPACE>: <COUNT>
<NAMESPACE>: <COUNT>
...
```

---

## Finds every unique root element and its frequency

* Query module: `defoe.generic_xml.queries.root_elements`
* Configuration file: None
* Result format:

```
<ELEMENT>: <COUNT>
<ELEMENT>: <COUNT>
...
```

---

## Counts total size of document files in bytes

* Query module: `defoe.generic_xml.queries.total_size`
* Configuration file: None
* Result format:

```
total_size: <TOTAL_SIZE>
```
