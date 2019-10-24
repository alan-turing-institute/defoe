# Demo - Queries for distribition of topics over time
Important: Here we use a list of queries to be submitted in a single spark job. The data is read and ingested a single time. 

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

#### List of Queries [defoe/run_queries.py]

Format:spark-submit --py-files defoe.zip defoe/run_queries.py <DATA_FILE> <DATA MODEL> -l <LIST_OF_QUERIES> -n <NUM_CORES>
 
Notes:
Data will be ingested once, and all the queries indicated in a file (e.g. query_distributed_topics.txt) will be run against the data in memory.
This way is much efficient, when we know already the list of queries to run. 

```bash
>> spark-submit --py-files defoe.zip defoe/run_queries.py nls_total_demo.txt nls -l query_distributed_topics.txt -n 324 
```

Important: In query_distributed_topics.txt I have the following

```bash
defoe.nls.queries.normalize -r results_nls_normalized
defoe.nls.queries.keysearch_by_year queries/sc_philosophers.yml -r results_ks_philosophers
defoe.nls.queries.keysearch_by_year queries/sport.ym -r results_ks_sports_normalize
defoe.nls.queries.keysearch_by_year queries/sc_cities.yml -r results_ks_cities
defoe.nls.queries.keysearch_by_year queries/animal.yml -r results_ks_animal
defoe.nls.queries.inventory_per_year -r results_inventory_per_year
```

For each query, I need to specify the full module path (e.g. defoe.nls.queries.normalize)
The configuration paramenters if it is needed (e.g. queries/sport.yml)
And the results file (e.g. results_ks_animal) --> by default it will generate a file called results_<NUM_QUERY>.yml if the user doesnt specify one


