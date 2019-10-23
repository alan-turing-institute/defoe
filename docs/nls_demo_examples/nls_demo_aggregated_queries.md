################### HOW TO REPLICATE THE QUERIES FOR THE STUDY OF DISTRIBUTION OF TOPICS OVER TIME ################
# 0. Requirements:
# 0.a) Dowload the nls full dataset ( https://data.nls.uk/data/digitised-collections/encyclopaedia-britannica/)
>>> wget https://nlsfoundry.s3.amazonaws.com/data/nls-data-encyclopaediaBritannica.zip 

# 0.b) How to generate nls_total_demo.txt
>>> find /mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica -maxdepth 1 -type d >& nls_total_demo.txt
(And delete the first row: '/mnt/lustre/at003/at003/rfilguei2/nls-data-encyclopaediaBritannica')

####### List of  Queries [defoe/run_queries.py]
#Notes:
# Data will be ingested once, and all the queries indicated in a file (e.g. query_distributed_topics.txt) will be run against the data in memory.
# This way is much efficient, when we know already the list of queries to run. 

>> nohup spark-submit --py-files defoe.zip defoe/run_queries.py nls_total_demo.txt nls -l query_distributed_topics.txt -n 324 > log.txt &

#Important: In query_distributed_topics.txt I have the following
defoe.nls.queries.normalize -r results_nls_normalized
defoe.nls.queries.keysearch_by_year queries/sc_philosophers.yml -r results_ks_philosophers
defoe.nls.queries.keysearch_by_year queries/sport.ym -r results_ks_sports_normalize
defoe.nls.queries.keysearch_by_year queries/sc_cities.yml -r results_ks_cities
defoe.nls.queries.keysearch_by_year queries/animal.yml -r results_ks_animal
defoe.nls.queries.inventory_per_year -r results_inventory_per_year

#For each query, I need to specify the full module path (e.g. defoe.nls.queries.normalize)
#The configuration paramenters if it is needed (e.g. queries/sport.yml)
#And the results file (e.g. results_ks_animal) --> by default it will generate a file called results_<NUM_QUERY>.yml if the user doesnt specify one


