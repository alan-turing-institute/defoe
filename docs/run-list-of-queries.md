# Run several queries at once - Just one data ingestion

Several queries can be submitted at once, ingesting just the data once, to Spark as follows.

ZIP up the source code (Spark needs this to run the query):

```bash
zip -r defoe.zip defoe
```

Submit the source code to Spark along with information about your query:

```bash
spark-submit --py-files defoe.zip defoe/run_queries.py <DATA_FILE> <DATA MODEL> -l <LIST_OF_QUERIES> [-e <ERRORS FILE>][-n <NUM_CORES>]
```

where:

* `<DATA_FILE>` is a file that lists either URLs or file paths which are the files over which the query is to be run, one per line. Either URLs or file paths should be exclusively used, not both.
* `<MODEL_NAME>` specifies which text model is to be used, one of:
  - `books`: British Library Books
  - `papers`: British Library Newspapers
  - `fmp`: Find My Past Newspapers
  - `nzpp`: Papers Past New Zealand and Pacific newspapers
  - `generic_xml`: Arbitrary XML documents
  - `nls`: Arbitrary XML documents
  - For example, `books` tells the code that the data files listed in `data.txt` are books so should be parsed into a books data model.
* `<LIST_OF _QUERIES>` is a file that list the queries to be submitted. Each query is the name of a Python module implementing the query to run, for example `defoe.alto.queries.find_words_group_by_word` or `defoe.papers.queries.articles_containing_words`. The query must be compatible with the chosen model. Each query, can have also the following optional parametesr:
* `<QUERY_CONFIG_FILE>` is a query-specific configuration file. This is optional and depends on the query implementation.
* `<RESULTS_FILE>` is the query results file, to hold the query results in YAML format. If omitted the default is `results.yml`.


* `<ERRORS_FILE>` is the errors file, to hold information on any errors in YAML format. If omitted the default is `errors.yml`.
* `<NUM_CORES>` is the number of computer processor cores requested for the job. If omitted the default is 1.

**Note for Urika users**

* It is recommended that the value of 144 be used for `<NUM_CORES>`. This, with the number of cores per node, determines the number of workers/executors and nodes. As Urika has 36 cores per node, this would request 144/36 = 4 workers/executors and nodes.
* This is required as `spark-runner --total-executor-cores` seems to be ignored.

For example, to submit a query to search a set of books for occurrences of some words (e.g. "heart" or "hearts") and return the counts of these occurrences grouped by year, you could run:

```bash
spark-submit --py-files defoe.zip defoe/run_queries.py nls_data.txt nls -l query_distributed_topics.txt
```

Where `query_distributed_topics.txt` could be:
```bash
defoe.nls.queries.normalize -r results_nls_normalized
defoe.nls.queries.keysearch_by_year queries/sc_philosophers.yml -r results_ks_philosophers
defoe.nls.queries.keysearch_by_year queries/sport.ym -r results_ks_sports_normalize
defoe.nls.queries.keysearch_by_year queries/sc_cities.yml -r results_ks_cities
defoe.nls.queries.keysearch_by_year queries/animal.yml -r results_ks_animal
defoe.nls.queries.inventory_per_year -r results_inventory_per_year
```
And:
* `nls_data.txt` is the file with the paths to the encyclopaedia files to run the query over.


---

## Submit a job to Spark as a background process

To submit a job to Spark as a background process, meaning you can do other things while Spark is running your query, use `nohup` and capture the output from Spark in ` log.txt` file. For example:

```bash
nohup spark-submit --py-files defoe.zip defoe/run_queries.py <DATA_FILE> <DATA MODEL> -l <LIST_OF_QUERIES> [-e <ERRORS FILE>][-n <NUM_CORES>] > log.txt &
```

You can expect to see at least one `python` and one `java` process:

```bash
ps
```
```
   PID TTY          TIME CMD
...
 92250 pts/1    00:00:02 java
 92368 pts/1    00:00:00 python
...
```

**Caution:** If you see `<RESULTS_FILE>` then do not assume that the query has completed and prematurely copy or otherwise try to use that file. If there are many query results then it may take a while for these to be written to the file after it is opened. Check that the background job has completed before using `<RESULTS_FILE>`. 

---

## Check if any data files were skipped due to errors

If any problems arise in reading data files or converting these into objects before running queries then an attempt will be made to capture these errors and record them in the errors file (default name `errors.yml`). If present, this file provides a list of the problematic files and the errors that arose.

