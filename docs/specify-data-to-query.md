# Specify data to query

Spark needs to know the data which you want to run a query over. You need to create a plain-text file with a list of the paths to the data files to query.

## British Library Books dataset 

To run queries over this dataset, the file needs a list of the paths to the zip files corresponding to the books over which the query is to be run.

For example, suppose you want to run a query over two books:

```
1510_1699/000001143_0_1-20pgs__560409_dat.zip
1510_1699/000000874_0_1-22pgs__570785_dat.zip
```

If running on your local machine, your file would be as follows, where `<BLB>` is the path to the directory in your home directory, where you have the data:

```
<BLB>/1510_1699/000001143_0_1-20pgs__560409_dat.zip
<BLB>/1510_1699/000000874_0_1-22pgs__570785_dat.zip
```

If running on Urika, your file would be as follows:

```
/mnt/lustre/<project>/<project>/<username>/BLB/1510_1699/000001143_0_1-20pgs__560409_dat.zip
/mnt/lustre/<project>/<project>/<username>/BLB/1510_1699/000000874_0_1-22pgs__570785_dat.zip
```

You can write these files by hand.

Alternatively, you can use the bash `find` command, to create a list of all available files:

* On a local machine:

```bash
find <BLB> -name "*.zip" | sort > data.txt
```

* On Urika:

```bash
find /mnt/lustre/<project>/<project>/<username>/BLB -name "*.zip" | sort > data.txt
```

You can then filter this file to select subsets of data e.g. to select books in the folder `1510_1699` you can run:

```bash
grep 1510_1699 data.txt > data_1510_1699.txt
```

---

## British Library Newspapers dataset 

To run queries over this dataset, the file needs a list of the paths to the XML files corresponding to the newspapers over which the query is to be run.

For example, suppose you want to run a query over two newspapers:

```
0000164- The Courier and Argus/0000164_19070603.xml
0000164- The Courier and Argus/0000164_19151123.xml
```

If running on your local machine, your file would be as follows, where `<BLN>` is the path to the directory in your home directory, where you have the data:

```
<BLN>/Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml
<BLN>/Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml
```

If running on Urika, your file would be as follows:

```
/mnt/lustre/<project>/<project>/<username>/BLN/Part 1/0000164- The Courier and Argus/1907/0000164_19070603/0000164_19070603.xml
/mnt/lustre/<project>/<project>/<username>/BLN/Part 1/0000164- The Courier and Argus/1915/0000164_19151123/0000164_19151123.xml
```

You can write these files by hand.

Alternatively, you can use the bash `find` command, to create a list of all available files:

* On a local machine:

```bash
find <BLN> -name "*.xml" | sort > data.txt
```

* On Urika:

```bash
find /mnt/lustre/<project>/<project>/<username>/BLN -name "*.xml" | sort > data.txt
```

You can then filter this file to select subsets of data e.g. to select papers in the folder `0000164- The Courier and Argus/`, you can run:

```bash
grep "0000164-\ The\ Courier\ and\ Argus" data.txt > data.courier.txt
```

---

## Times Digital Archive dataset

To run queries over this dataset, the file needs a list of the paths to the XML files corresponding to the newspapers over which the query is to be run.

For example, suppose you want to run a query over two newspapers:

```
0FFO-1785-APR01.xml
0FFO-1785-APR02.xml
```

If running on your local machine, your file would be as follows, where `<TDA>` is the path to the directory in your home directory, where you have the data:

```
<TDA>/1785/17850401/0FFO-1785-APR01.xml
<TDA>/1785/17850402/0FFO-1785-APR02.xml
```

If running on Urika, your file would be as follows:

```
/mnt/lustre/<project>/<project>/<username>/TDA/1785/17850401/0FFO-1785-APR01.xml
/mnt/lustre/<project>/<project>/<username>/TDA/1785/17850402/0FFO-1785-APR02.xml
```

You can write these files by hand.

Alternatively, you can use the bash `find` command, to create a list of all available files:

* On a local machine:

```bash
find <TDA> -name "*.xml" | sort > data.txt
```

* On Urika:

```bash
find /mnt/lustre/<project>/<project>/<username>/TDA -name "*.xml" | sort > data.txt
```

---

## Papers Past New Zealand and Pacific newspapers dataset

To run queries over this dataset, the file needs a list of the paths to the XML files corresponding to the newspapers over which the query is to be run.

For example, suppose you want to run a query over two documents:

```
1000.xml
1001.xml
```

If running on your local machine, your file would be as follows, where `<NZPP>` is the path to the directory in your home directory, where you have the data:

```
<NZPP>/1000.xml
<NZPP>/1001.xml
```

If running on Urika, your file would be as follows:

```
/mnt/lustre/<project>/<project>/<username>/NZPP/1000.xml
/mnt/lustre/<project>/<project>/<username>/NZPP/1001.xml
```

You can write these files by hand.

Alternatively, you can use the bash `find` command, to create a list of all available files:

* On a local machine:

```bash
find <NZPP> -name "*.xml" | sort > data.txt
```

* On Urika:

```bash
find /mnt/lustre/<project>/<project>/<username>/NZPP -name "*.xml" | sort > data.txt
```

---

## Arbitrary XML documents

To run queries over arbitrary XML documents, the file needs a list of the paths to the XML files.

This can be created as for the British Library Newspapers dataset above.
