################### HOW TO REPLICATE THE QUERIES FOR THE STUDY OF DISTRIBUTION OF TOPICS OVER TIME ################
# 0. Requirements:
# 0.a) Dowload the nls full dataset ( https://data.nls.uk/data/digitised-collections/encyclopaedia-britannica/)
>>> wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-encyclopaediaBritannica.zip 

# 0.b) How to generate nls_total_demo.txt
>>> find /mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica -maxdepth 1 -type d >& nls_total_demo.txt
(And delete the first row: '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica')

####### Individual Queries [defoe/run_query.py]
#Format:spark-submit --py-files defoe.zip defoe/run_query.py <DATA_FILE> <MODEL_NAME> <QUERY_NAME> <QUERY_CONFING> -r <RESULTS> -n <NUM_CORES>
 
#Notes:
#Everytime I run a query (e.g. defoe.nls.queries.total_documents or defoe.nls.queries.normalize), defoe loads read data from files to memory,
#and it will later run the query. So, each time the data is read, ingested, queried. 

#1. Total_documents
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.total_documents  -r results_total_documents -n 324 > log.txt &

#2. Normalize query- It gets the total of documents, pages, words groupped by year
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.normalize  -r results_norm -n 324 > log.txt & 

#3. Keysearch by topics [sport, philosophers, cities, animals] - group by year

#3.1 Sports - normalize preprocessing (check queries/sport.yml to see the preprocessing treatments)
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sport.yml -r results_ks_sports -n 324 > log.txt & 

#3.2 Scottish Philosophers - normalization and lemmatization (normalization is applied first always if lemmatization or stemming is selected) preprocessing (check queries/sc_philosophers to see the preprocessing treatment)

>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sc_philosophers.yml -r results_ks_philosophers -n 324 > log.txt & 

#3.3 Cities - normalization and lemmatization (check queries/sc_cities.yml)
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/sc_cities.yml -r results_ks_cities -n 324 > log.txt

#3.4 Animals - normalization and lemmatization(check)
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.keysearch_by_year queries/animal.yml -r results_ks_animal -n 324 > log.txt

#4. Getting the inventory per year [title and edition]
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_total_demo.txt nls defoe.nls.queries.inventory_per_year -r results_inventory_per_year -n 324 > log.txt &

############################# Work in Progess ##################################
### ATENTION: The following queries might change during the next weeks

#Writing preprocessed pages to HDFS file - we have to indicate the HDFS FILE inside write_preprocessed_HDFS
#Note: We have another query, called write_pages_HDFS, that writes "raw" data (without preprocessing them) into HDFS FILE
 
>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py nls_tiny.txt nls defoe.nls.queries.write_pages_preprocessed_HDFS queries/preprocess.yml -r results -n 324 > log.txt &
# Important  --> We collect the following metadata per page (and also the page as string): tittle, edition, year, place, archive filename, page filename, page id, num pages, type of archive, model, type of preprocess treatment, page_preprocessed_as_string

#Checking results from HDFS file

>>> hdfs dfs -cat /user/at003/rosa/<NAME OF THE HDFS FILE>.txt/part-00323 > encyclo_prep_norm 
#Read preprocessed pages to HDFS file and do a keysentence search - group by year
Important: in hdfs_data.txt we have to indicate the HDFS file that we want to read from: --> hdfs:///user/at003/rosa/<NAME OF THE HDFS FILE>.txt

>>> nohup spark-submit --py-files defoe.zip defoe/run_query.py hdfs_data.txt hdfs defoe.hdfs.queries.read_pages_from_HDFS queries/sport.yml  -r results_ks_sports_tiny -n 324 > log.txt &

############ Spark in a SHELL - Pyspark #########
>>> nls_data = sc.textFile("hdfs:///user/at003/rosa/<NAME OF THE HDFS FILE>.txt")
>>> nls_sample = nls_data.take(10)
>>> entry=nls_sample[8][1:-1].split("\',")
>>> clean_entry=[item.split("\'")[1] for item in entry]
>>> year = int(clean_entry[2])
>>> page_as_string = clean_entry[11]

