# Demo - Queries for distribition of topics over time

Important: Here, for each query we read the data from files to memory, run the query, and then gets the results.

#### Requirements:
* Dowload the nls full dataset ( https://data.nls.uk/data/digitised-collections/encyclopaedia-britannica/)
```bash
 wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-encyclopaediaBritannica.zip 
```
And **unzipped** it later.

* How to generate nls_total_demo.txt
```bash
 find /mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica -maxdepth 1 -type d >& nls_total_demo.txt
```
(And delete the first row: '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica')

* Install Spark and Java 8 
```bash
 sudo apt install openjdk-8-jdk
 wget http://apache.mirror.anlx.net/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
 tar xvf spark-2.4.2-bin-hadoop2.7.tgz
```

* Install defoe
```bash
 https://github.com/alan-turing-institute/defoe.git
 conda create -n mypy27 python=2.7 anaconda
 conda activate mypy27
 conda update -n base -c defaults conda
 ./requirements.sh
 pip install Pillow==4.0.0
 python
 >> import nltk
 >> nltk.download('wordnet')
```

* Zip defoe code:
```bash
   cd defoe
   zip -r defoe.zip defoe
```

####  Individual Queries [defoe/run_query.py]

Format:spark-submit --py-files defoe.zip defoe/run_query.py <DATA_FILE> <MODEL_NAME> <QUERY_NAME> <QUERY_CONFING> -r <RESULTS> -n <NUM_CORES>
 
Notes:
Everytime we run a query (e.g. defoe.nls.queries.total_documents or defoe.nls.queries.normalize), defoe loads/reads data from files into memory, and later the query is run. So, each time the data is read, ingested, queried. 

* Total_documents
```bash
  spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.total_documents  -r results_total_documents -n 324 

```
* Normalize query- It gets the total of documents, pages, words groupped by year
```bash
  spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.normalize  -r results_norm -n 324  
```

* Keysearch by topics [sport, philosophers, cities, animals] - group by year

	* Sports - normalize preprocessing (check queries/sport.yml to see the preprocessing treatments)
	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sport.yml -r results_ks_sports -n 324  
	```

	* Scottish Philosophers - normalization and lemmatization (normalization is applied first always if lemmatization or stemming is selected) preprocessing (check queries/sc_philosophers to see the preprocessing treatment)

	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sc_philosophers.yml -r results_ks_philosophers -n 324  
	```

	* Cities - normalization and lemmatization (check queries/sc_cities.yml)
	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sc_cities.yml -r results_ks_cities -n 324 > log.txt
	```

	* Animals - normalization and lemmatization(check)
	```bash
 	 spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/animal.yml -r results_ks_animal -n 324 > log.txt
	```
* Getting the inventory per year [title and edition]
```bash
  spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.inventory_per_year -r results_inventory_per_year -n 324 
```

# Writing and Reading data from/to HDFS

Writing [pages to HDFS cvs file using dataframes](https://github.com/alan-turing-institute/defoe/blob/master/defoe/nls/queries/write_pages_df_hdfs.py) loads in memory all the pages and their metadata, applies all type of preprocess treatment ot the pages, create a dataframe, store data into the dataframe, and finally save the dataframe into HDFS using a csv file.  

The information stored per page is the following:
"title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem", "num_words". 

In “source_text_clean”, I store the result of applying two modifications to the raw text (source_text_raw): 1) Handle hyphenated words and 2) fix the long-s. The pre-process treatments (*normalize*, *stem* and *lemmatize*) are applied to text stored in this field, and not from the raw one. Both, *stem* and *lemmatize*, they also include normalization.  . 


We have to indicate the HDFS FILE inside **write_pages_df__hdfs.py** (e.g. "nls_demo.csv"). 

  

```bash
 nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_tiny.txt nls defoe.nls.queries.write_pages_df_hdfs  -r results -n 324 > log.txt &
```


**Important** --> nls_tiny.txt is:
```bash
xxx/nls-data-encyclopaediaBritannica/193108323
xxx/nls-data-encyclopaediaBritannica/193696080
xxx/nls-data-encyclopaediaBritannica/144850378
xxx/nls -data-encyclopaediaBritannica/191253839
xxx/nls -data-encyclopaediaBritannica/144133902
xxx/nls -data-encyclopaediaBritannica/144850368
xxx/nls -data-encyclopaediaBritannica/190273291
xxx/nls -data-encyclopaediaBritannica/191253819
xxx/nls -data-encyclopaediaBritannica/191678900
xxx/nls -data-encyclopaediaBritannica/192984259
xxx/nls -data-encyclopaediaBritannica/193819047
xxx/nls -data-encyclopaediaBritannica/191678897
xxx/nls -data-encyclopaediaBritannica/192547788
xxx/nls -data-encyclopaediaBritannica/193916150
```

* Checking results from HDFS file

```bash
 hdfs dfs -getmerge /user/at003/rosa/nls_demo.csv nls_demo.csv
```

Read pages (preprocessed or raw) as Dataframes from HDFS CSV file, and do a [keysentence search](https://github.com/alan-turing-institute/defoe/blob/master/defoe/hdfs/queries/keysearch_by_year.py) groupping results by year.

In [hdfs_data.txt](https://github.com/alan-turing-institute/defoe/blob/master/hdfs_data.txt) we have to indicate the HDFS file that we want to read from (e.g. hdfs:///user/at003/rosa/nls_demo.csv)
	
In the configuration file (e.g.[queries/sport.yml](https://github.com/alan-turing-institute/defoe/blob/master/queries/sport.yml)) we have to indicate which preprocess treatment (e.g. none, normalize, etc.) we want to use in the query, so we can select the dataframe's columm (e.g. *page_string_raw*, *page_string_normalize*, etc.) according to that. 

```bash
queries/sport.yml: 
	preprocess: normalize
	data: sport.txt
```

```bash
  spark-submit --py-files defoe.zip defoe/run_query.py hdfs_data.txt hdfs defoe.hdfs.queries.keysearch_by_year queries/sport.yml  -r results_ks_sports_tiny -n 324 
```


```bash
results_ks_sports_tiny:
'1771':
- [bowls, 3]
'1773':
- [tennis, 1]
'1797':
- [golf, 1]
- [football, 1]
- [rugby, 1]
- [bowls, 1]
'1810':
- [tennis, 15]
- [bowls, 1]
'1815':
- [football, 1]
'1823':
- [bowls, 2]
- [tennis, 2]
'1824':
- [bowls, 1]
'1842':
- [bowls, 5]
- [football, 2]
- [rugby, 1]
'1853':
- [rugby, 8]
- [bowls, 4]
- [tennis, 1]
- [football, 1]

```


# Writing and Reading data from/to PostgreSQL database 

Writing [pages to PostgresSQL database using dataframes](https://github.com/alan-turing-institute/defoe/blob/master/defoe/nls/queries/write_pages_df_psql.py) loads in memory all the pages and their metadata, applies all type of preprocess treatment ot the pages, create a dataframe, store data into the dataframe, and finally save the dataframe into a database table. Properties of the database to use can be specified by using a config file (e.g. [queries/db_properties.yml](https://github.com/alan-turing-institute/defoe/blob/master/queries/db_properties.yml))

The information stored per page is the following:
"title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem", "num_words". 

In “source_text_clean”, I store the result of applying two modifications to the raw text (source_text_raw): 1) Handle hyphenated words and 2) fix the long-s. The pre-process treatments (*normalize*, *stem* and *lemmatize*) are applied to text stored in this field, and not from the raw one. Both, *stem* and *lemmatize*, they also include normalization.  . 


```bash
spark-submit --driver-class-path $HOME/postgresql-42.2.8.jar --jars $HOME/postgresql-42.2.8.jar --py-files defoe.zip defoe/run_query.py nls_tiny.txt nls defoe.nls.queries.write_pages_df_psql queries/db_properties.yml  -r results -n 324 
```

Notice that the properties of the database to use are indicated in a file --> queries/db_properties.yml:

```bash
host: ati-nid00006
port: 55555
database: defoe_db
table: publication_page
user: rfilguei2
```


Important:
* You need to have the postgresql driver, or [download it](https://jdbc.postgresql.org/) and indicate it in the spark-submit command (see previous command). 

* You need to have previously the postgreSQL database created- [See extended notes](https://github.com/alan-turing-institute/defoe/blob/master/defoe/psql/postgreSQL_Spark_Notes.txt). However, the table will be created automatically. 


```bash
psql -d defoe_db 

\d+
                          List of relations
 Schema |       Name       | Type  |   Owner   |  Size  | Description 
--------+------------------+-------+-----------+--------+-------------
 public | publication_page | table | rfilguei2 | 138 MB | 
(1 row)

defoe_db=# \d+ publication_page
                                     Table "public.publication_page"
        Column         |  Type  | Collation | Nullable | Default | Storage  | Stats target | Description 
-----------------------+--------+-----------+----------+---------+----------+--------------+-------------
 title                 | text   |           |          |         | extended |              | 
 edition               | text   |           |          |         | extended |              | 
 year                  | bigint |           |          |         | plain    |              | 
 place                 | text   |           |          |         | extended |              | 
 archive_filename      | text   |           |          |         | extended |              | 
 source_text_filename  | text   |           |          |         | extended |              | 
 text_unit             | text   |           |          |         | extended |              | 
 text_unit_id          | text   |           |          |         | extended |              | 
 num_text_unit         | bigint |           |          |         | plain    |              | 
 type_archive          | text   |           |          |         | extended |              | 
 model                 | text   |           |          |         | extended |              | 
 source_text_raw       | text   |           |          |         | extended |              | 
 source_text_clean     | text   |           |          |         | extended |              | 
 source_text_norm      | text   |           |          |         | extended |              | 
 source_text_lemmatize | text   |           |          |         | extended |              | 
 source_text_stem      | text   |           |          |         | extended |              | 
 num_words             | bigint |           |          |         | plain    |              | 
 
  
```

Read pages (preprocessed or raw) as Dataframes from PostgreSQL database, and do a [keysentence search](https://github.com/alan-turing-institute/defoe/blob/master/defoe/psql/queries/keysearch_by_year.py) groupping results by year.

In the configuration file (e.g.[queries/sport.yml](https://github.com/alan-turing-institute/defoe/blob/master/queries/sport.yml)) we have to indicate which preprocess treatment (e.g. none, normalize, etc.) we want to use in the query, so we can select the dataframe's columm (e.g. *page_string_raw*, *page_string_normalize*, etc.) according to that. 

```bash
spark-submit --driver-class-path $HOME/postgresql-42.2.8.jar --jars $HOME/postgresql-42.2.8.jar --py-files defoe.zip defoe/run_query.py db_data.txt psql defoe.psql.queries.keysearch_by_year queries/sport.yml  -r results_ks_sports_tiny -n 324
```
Important: A file with the database properties has to be specified (e.g.[db_data.txt](https://github.com/alan-turing-institute/defoe/blob/master/db_data.txt)). It has to have the following information (and in this order), separated by comma: 

#host,port,db_name,user,driver,table_name
ati-nid00006,55555,defoe_db,rfilguei2,org.postgresql.Driver,publication_page



# Writing data to ElasticSearch (ES) 

Writing [pages to ES  using dataframes](https://github.com/alan-turing-institute/defoe/blob/master/defoe/nls/queries/write_pages_df_es.py) loads in memory all the pages and their metadata, applies all type of preprocess treatment ot the pages, create a dataframe, store data into the dataframe, and finally save the dataframe into ES. P

The information stored per page is the following:
"title",  "edition", "year", "place", "archive_filename",  "source_text_filename", "text_unit", "text_unit_id", "num_text_unit", "type_archive", "model", "source_text_raw", "source_text_clean", "source_text_norm", "source_text_lemmatize", "source_text_stem", "num_words". 

In “source_text_clean”, I store the result of applying two modifications to the raw text (source_text_raw): 1) Handle hyphenated words and 2) fix the long-s. The pre-process treatments (*normalize*, *stem* and *lemmatize*) are applied to text stored in this field, and not from the raw one. Both, *stem* and *lemmatize*, they also include normalization.  . 


```bash
spark-submit --driver-class-path elasticsearch-hadoop-7.5.0/dist/elasticsearch-hadoop-7.5.0.jar --jars elasticsearch-hadoop-7.5.0/dist/elasticsearch-hadoop-7.5.0.jar  --py-files defoe.zip defoe/run_query.py nls-data.txt nls defoe.nls.queries.write_pages_df_es queries/es_properties.yml -r results -n 324
```

Notice that the properties of index and type name for ES are indicated in a file --> queries/es_properties.yml:


```bash
index: nls
type_name: Encyclopaedia_Britannica
```

Important:
* You need to have the elasticsearch-hadoop driver, or [download it](https://www.elastic.co/downloads/hadoop) and indicate it in the spark-submit command (see previous command). 



# Spark in a SHELL - Pyspark 

Reading **dataframes** from *HDFS*:
```bash
 >> df= sqlContext.read.csv("hdfs:///user/at003/rosa/nls_demo.csv", header="true")
 >> def blank_as_null(x):
...     return when(col(x) != "", col(x)).otherwise(None)
>> fdf = df.withColumn("page_string_norm", blank_as_null("page_string_norm"))
 
>> newdf=fdf.filter(fdf.page_string_raw.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.page_string_raw)
>> pages=newdf.rdd.map(tuple)
>> nls_sample=pages.take(8)
>> entry= nls_sample[8]
>> year = entry[0]
>> page_as_string = entry[1]
 
```

Reading **dataframes** from *PostgreSQL*:
```bash
pyspark --driver-class-path postgresql-42.2.8.jar --jars postgresql-42.2.8.jar
from pyspark.sql import DataFrameReader

>> from pyspark.sql import DataFrameReader
>> from pyspark.sql.functions import when, col
>> url = 'postgresql://ati-nid00006:55555/defoe_db'
>> properties = {'user': 'rfilguei2', 'driver': 'org.postgresql.Driver'}
>> df = DataFrameReader(sqlContext).jdbc(url='jdbc:%s' % url, table='publication_page' , properties=properties)
>> def blank_as_null(x):
...     return when(col(x) != "", col(x)).otherwise(None)
>> fdf = df.withColumn("page_string_norm", blank_as_null("source_text_norm"))
 
>> newdf=fdf.filter(fdf.source_text_raw.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.source_text_raw)
>> pages=newdf.rdd.map(tuple)
>> nls_sample=pages.take(8)
>> entry= nls_sample[8]
>> year = entry[0]
>> page_as_string = entry[1]
```

Reading **dataframes** from *ES*:
```bash
pyspark --jars elasticsearch-hadoop-7.5.0/dist/elasticsearch-hadoop-7.5.0.jar 
>> from pyspark.sql.functions import when, col
>> reader = spark.read.format("org.elasticsearch.spark.sql").option("es.read.metadata", "true").option("es.nodes.wan.only","true").option("es.port","9200").option("es.net.ssl","false").option("es.nodes", "http://localhost")
>> df = reader.load("nls/Encyclopaedia_Britannica")
>> def blank_as_null(x):
...     return when(col(x) != "", col(x)).otherwise(None)
>> fdf = df.withColumn("page_string_norm", blank_as_null("source_text_norm"))
 
>> newdf=fdf.filter(fdf.source_text_raw.isNotNull()).filter(fdf["model"]=="nls").select(fdf.year, fdf.source_text_raw)
>> pages=newdf.rdd.map(tuple)
>> nls_sample=pages.take(8)
>> entry= nls_sample[8]
>> year = entry[0]
>> page_as_string = entry[1]
```


Reading **rdds**:
```bash
>> nls_data = sc.textFile("hdfs:///user/at003/rosa/<NAME OF THE HDFS FILE>.txt")
>> nls_sample = nls_data.take(10)
>> entry=nls_sample[8][1:-1].split("\',")
>> clean_entry=[item.split("\'")[1] for item in entry]
>> year = int(clean_entry[2])
>> preprocess_type = clean_entry[10]
>> page_as_string = clean_entry[11]
```




