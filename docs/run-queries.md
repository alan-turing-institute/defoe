# Run queries

To run a query on Spark you need to create a job bundle, which contains:

* A list of the paths to the data files to query. This is described in [Specify data to query](./specify-data.md).
* The code in this directory, which parses the data and runs the query.
* The code that implements the query.
* A configuration file which provides the query code with additional information (e.g. words to search for).

Here we describe how to create the job bundle and submit a job to Spark to run the query.

---

## Create a job bundle

We provide a `create_job.py` tool to create the bundle. Its arguments are as follows:

```
usage: create_job.py [-h] job data model query [config]

Create Spark query job bundle

positional arguments:
  job_dir     Directory to create to hold job bundle
  data        Data file listing data files to query
  model       Data model to which data files conform: ['books', 'papers']
  query       Python query file
  config      Query-specific configuration file

optional arguments:
  -h, --help  show this help message and exit
```

For example, to create a job bundle to run a query to search a set of books for occurrences of some words (e.g. "heart" or "hearts") and return the counts of these occurrences grouped by year, you could run:

```bash
python lwm/create_job.py job-books data.txt books queries/books/find_words_group_by_year.py queries/config/hearts.txt
```

where:

* `job-books` is the directory within which the job bundle is created.
* `data.txt` is the file with the paths to the books files to run the query over.
* `books` tells the code that the data files listed in `data.txt` are books so should be parsed into a books data model.
* `queries/books/find_words_group_by_year.py` is the code that runs the query.
* `queries/config/hearts.txt` is a configuration file for the query which contains a list of the words, one per line, to search for.

For example, to create a job bundle to run a query to search a set of newspapers for occurrences of gender-specific words (e.g. "she", "he" etc.) and return the counts of these occurrences grouped by year, you could run:

```bash
python lwm/create_job.py job-papers data.txt papers queries/papers/articles_containing_words.py queries/config/gender.txt
```

where:

* `job-papers` is the directory within which the job bundle is created.
* `data.txt` is the file with the paths to the newspapers files to run the query over.
* `papers` tells the code that the data files listed in `data.txt` are newspapers so should be parsed into a newspapers data model.
* `queries/papers/articles_containing_words.py` is the code that runs the query.
* `queries/config/gender.txt` is a configuration file for the query, which contains a list of the words, one per line, to search for.

---

## Submit a job to Spark

Having created a job bundle, it can be submitted to Spark as follows.

```bash
cd <JOB_BUNDLE_DIRECTORY>
spark-submit --py-files lwm.zip lwm/query_runner.py [<NUM_CORES>]
```

where:

* `<JOB_BUNDLE_DIRECTORY>` is the job bundle directory created earlier.
* `<NUM_CORES>` is the number of computer processor cores requested for the job. If omitted the default is 1.

**Note for Urika users**

* It is recommended that the value of 144 be used for `<NUM_CORES>`. This, with the number of cores per node, determines the number of workers/executors and nodes. As Urika has 36 cores per node, this would request 144/36 = 4 workers/executors and nodes.
* This is required as `spark-runner --total-executor-cores` seems to be ignored.

For example, to submit the job bundle to run the query to search a set of books for occurrences of some words (e.g. "heart" or "hearts") and return the counts of these occurrences grouped by year, you could run:

```bash
cd job-book
spark-submit --py-files lwm.zip lwm/query_runner.py
```

For example, to submit the job bundle to run the query to search a set of newspapers for occurrences of gender-specific words (e.g. "she", "he" etc.) and return the counts of these occurrences grouped by year, you could run:

```bash
cd job-papers
spark-submit --py-files lwm.zip lwm/query_runner.py
```

If successful the results will be written into a new file (commonly called `results.yml`) in the job bundle directory.

---

## Submit a job to Spark as a background process

To submit a job to Spark as a background process, meaning you can do other things while Spark is running your query, use `nohup` and capture the output from Spark in ` log.txt` file. For example:

```bash
nohup spark-submit --py-files lwm.zip lwm/query_runner.py 144 > log.txt &
```

---

## Check number of executors used

A quick-and-dirty way to check the number of executors used is, if you have used `nohup` and output capture to `log.txt`, to run:

```bash
grep Exec log.txt | wc -l
```

---

## Troubleshooting: `No such file or directory: ''` and `Error reading file: ''`
If you get an error like:

```
IOError: [Errno 2] No such file or directory: ''
```

or:

```
IOError: Error reading file '': failed to load external entity ""
```

then check for blank lines in your data file and, if there are any, then remove them.

---

## Troubleshooting: `result.yml` is `{}`

If you run:

```bash
head result.yml
```

and see:

```
{}
```

then check the permissions of the data files. This can arise if, for example, a data file has permissions like:

```bash
ls -l /mnt/lustre/<user>/blpaper/0000164_19010101.xml
```
```
---------- 1 <user> at01 3374189 May 31 13:57
```
