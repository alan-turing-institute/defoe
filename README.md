# "Defoe" - analysis of historical books and newspapers data

This repository contains code to analyse historical books and newspapers datasets using Apache Spark. 

---

## Supported datasets

### British Library Books

This dataset consists of ~1TB of digitised versions of ~68,000 books from the 16th to the 19th centuries. The books have been scanned into a collection of XML documents. Each book has one XML document one per page plus one XML document for metadata about the book as a whole. The XML documents for each book are held within a compressed, ZIP, file. These ZIP files occupy ~224GB.

This dataset is available under an open, public domain, licence. See [Datasets for content mining](https://www.bl.uk/collection-guides/datasets-for-content-mining) and [BL Labs Flickr Data: Book data and tag history (Dec 2013 - Dec 2014)](https://figshare.com/articles/BL_Labs_Flickr_Data/1269249). For links to the data itself, see [Digitised Books largely from the 19th Century](https://data.bl.uk/digbks/). The data is provided by [Gale](https://www.gale.com), a division of [CENGAGE](https://www.cengage.com/).

### British Library Newspapers

This dataset consists of ~1TB of digitised versions of newspapers from the 18th to the early 20th century. Each newspaper has an associated folder of XML documents where each XML document corresponds to a single issue of the newspaper. Each XML document conforms to a British Library-specific XML schema.

This dataset is available, under licence, from [Gale](https://www.gale.com), a division of [CENGAGE](https://www.cengage.com/). The dataset is in 5 parts e.g. [Part I: 1800-1900](https://www.gale.com/uk/c/british-library-newspapers-part-i). For links to all 5 parts, see [British Library Newspapers](https://www.gale.com/uk/s?query=british+library+newspapers). 

### Times Digital Archive

The code can also handle the [Times Digital Archive](https://www.gale.com/uk/c/the-times-digital-archive) (TDA). 

This dataset is available, under licence, from [Gale](https://www.gale.com), a division of [CENGAGE](https://www.cengage.com/).

---

# Get started

Set up:

* [Set up local environment](docs/setup-local.md)
* [Set up Urika environment](docs/setup-urika.md)

Run queries:

* [Specify data to query](docs/specify-data.md)
* [Run queries](docs/run-queries.md)

Available queries:

* [ALTO document queries](docs/alto-queries) (British Library Books dataset)
* [British Library Newspapers](docs/papers-queries.md) (these can also be run on the Times Digital Archive)

Developers:

* [Run unit tests](docs/tests.md)

---

## Origins and acknowledgements

### British Library Books analysis code

The code to analyse the British Library Books dataset has its origins in the first phase of '[Enabling Complex Analysis of Large Scale Digital Collections](http://figshare.com/articles/Enabling_Complex_Analysis_of_Large_Scale_Digital_Collections/1319482)', a project funded by the [Jisc Research Data Spring](https://www.jisc.ac.uk/rd/projects/research-data-spring) in 2015.

The project team included: Melissa Terras (UCL), James Baker (British Library), David Beavan (UCL), James Hetherington (UCL), Martin Zaltz Austwick (UCL), Oliver Duke-Williams (UCL), Will Finley (University of Sheffield), Helen O'Neill (UCL), Anne Welsh (UCL).

See the GitHub repository, [UCL-dataspring/cluster-code](https://github.com/UCL-dataspring/cluster-code).

### Times Digital Archive and British Library Newspapers analysis code

The code to analyse the Times Digital Archive and British Library Newspapers dataset has its origins in code developed by [UCL](https://www.ucl.ac.uk/) to analyse the Times Digital Archive. This work took place from 2016-2018.

The project team included: James Hetherington (UCL), Raquel Alegre (UCL), Roma Klapaukh (UCL).

See the GitHub repository, [UCL/i_newspaper_rods](https://github.com/UCL/i_newspaper_rods)

### Analysing humanities data using Cray Urika-GX

Both codes were updated and extended by [EPCC](https://www.epcc.ed.ac.uk) as part of the [Research Engineering Group](https://www.turing.ac.uk/research/research-engineering) of the [The Alan Turing Institute](https://www.turing.ac.uk). The work focused on running both codes on the [Alan Turing Institute Cray Urika-GX Service](https://ati-rescomp-service-docs.readthedocs.io/en/latest/cray/introduction.html).

This work was done in conjunction with Melissa Terras, College of Arts, Humanities and Social Sciences (CAHSS), The University of Edinburgh. The work was funded by Scottish Enterprise as part of the Alan Turing Institute-Scottish Enterprise Data Engineering Program. This work took place from 2018-2019.

The project team included: Rosa Filgueira (EPCC), Mike Jackson (EPCC)

See the GitHub repositories:

* [alan-turing-institute/cluster-code (branch:epcc-sparkrods)](https://github.com/alan-turing-institute/cluster-code/tree/epcc-sparkrods)
* [alan-turing-institute/i_newspaper_rods (branch:epcc-master)](https://github.com/alan-turing-institute/i_newspaper_rods/tree/epcc-master)

---

## Name

The code is called "defoe" after [Daniel Defoe](https://en.wikipedia.org/wiki/Daniel_Defoe), writer, journalist and pamphleteer of the 17-18 century.

---

## Copyright and licence

Copyright (c) 2015-2018 University College London

Copyright (c) 2018-2019 The University of Edinburgh

All code is available for use and reuse under a [MIT Licence](http://opensource.org/licenses/MIT). See [LICENSE](./LICENSE).

### Data

The file defoe/test/books/fixtures/000000037_0_1-42pgs__944211_dat_modified.zip is a modified copy of the file 000000037_0_1-42pgs__944211_dat.zip from [OCR text derived from digitised books published 1880 - 1889 in ALTO XML](https://data.bl.uk/digbks/db11.html) (doi: 10.21250/db11) which is licenced under [CC0 1.0 Public Domain](https://creativecommons.org/licenses/by/4.0/).

The modifications are as follows:

000000037_metadata.xml:

```
-               <MODS:placeTerm type="text">Manchester</MODS:placeTerm>
=>
+               <MODS:placeTerm type="text">Manchester [1823]</MODS:placeTerm>
```

000000218_metadata.xml:

```
-               <MODS:placeTerm type="text">London</MODS:placeTerm>
+               <MODS:placeTerm type="text">London [1823]</MODS:placeTerm>
```
