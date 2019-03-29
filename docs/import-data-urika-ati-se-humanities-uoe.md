# Import British Library Books and Newspapers data into Urika

**Note:** This information applies to Alan Turing Institute-Scottish Enterprise Data Engineering Program University of Edinburgh project members only.

---

## Important

Do **not** mount DataStore directories directly onto Lustre.

---

## Copy British Library Books dataset

Space required: ~224 GB

Mount CAHSS Digital Cultural Heritage DataStore directory into your home directory on Urika:

```bash
mkdir dch
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@chss.datastore.ed.ac.uk:/chss/datastore/chss/groups/Digital-Cultural-Heritage dch
```

Copy XML files only and set permissions in copy to be user-readable only:

```bash
nohup rsync -rq --include "*/" --include "0*.zip" --exclude "*" --chmod=Du=rwx,Dgo=,Fu=rwx,Fgo= dch/BritishLibraryBooks/1* /mnt/lustre/<project>/<project>/<username>/BLB &
```

You can optionally validate the transfer as follows:

* Get file names in your local copy:

```bash
cd /mnt/lustre/<project>/<project>/<username>
find BLB -name "*.zip" > blb.txt
cut -d "/" -f3 blb.txt | sort > blb-files.txt
wc -l blb-files.txt
```
```
63700 blb-files.txt
```

* Get file names from DataStore:

```bash
find ~/dch/BritishLibraryBooks/1* -name "0*zip" > mount-blb.txt
cut -d "/" -f8 mount-blb.txt | sort > mount-blb-files.txt
wc -l mount-blb-files.txt
```
```
63700 mount-blb-files.txt
```

* Compare:

```
cmp blb-files.txt mount-blb-files.txt
```

`cmp` should display nothing, indicating that the contents are the same.

---

## Copy British Library Newspapers dataset

Space required: ~424 GB

Mount Library British Library Newspapers DataStore directory into your home directory on Urika:

```bash
mkdir blpaper
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@sg.datastore.ed.ac.uk:/sg/datastore/lib/groups/lac-store/blpaper blpaper
```

Copy XML files only and set permissions in copy to be user-readable only:

```bash
nohup rsync -rq --exclude "xmlonly" --include "*/" --include "*.xml" --exclude "*" --chmod=Du=rwx,Dgo=,Fu=rw,Fgo= blpaper/Part* /mnt/lustre/<project>/<project>/<username>/BLN &
```

You can optionally validate the transfer as follows:

* Get file names in your local copy:

```bash
cd /mnt/lustre/<project>/<project>/<username>
for P in 1 2 3; do find BLN/Part\ $P/ -name "*.xml" > bln-pt$P.txt ; done
for P in 4 5 6; do find BLN/Part$P/ -name "*.xml" > bln-pt$P.txt ; done
wc -l bln-pt*
```
```
   28642 bln-pt1.txt
   29754 bln-pt2.txt
   34048 bln-pt3.txt
   29785 bln-pt4.txt
   35639 bln-pt5.txt
   21801 bln-pt6.txt
  179669 total
```
```bash
# Part 1,2,3 differs in directory nesting from 4,5,6 so reverse to ensure file name is in first column, slice out file name, then reverse back.
for P in 1 2 3 4 5 6; do rev bln-pt$P.txt | cut -d "/" -f1 | rev | sort >> bln-files-tmp.txt ; done
sort bln-files-tmp.txt > bln-files.txt
rm bln-files-tmp.txt
wc -l bln-files.txt
```
```
179669 bln-files.txt
```

* Get file names from DataStore:

```bash
for P in 1 2 3; do find ~/blpaper/Part\ $P -name "*.xml" | grep -v "xmlonly" > mount-bln-pt$P.txt ; done &
for P in 4 5 6; do find ~/blpaper/Part$P -name "*.xml" | grep -v "xmlonly" > mount-bln-pt$P.txt ; done &
wc -l mount-bln-*
```
```
   28642 mount-bln-pt1.txt
   29754 mount-bln-pt2.txt
   34048 mount-bln-pt3.txt
   29785 mount-bln-pt4.txt
   35639 mount-bln-pt5.txt
   21801 mount-bln-pt6.txt
  179669 total
```
```bash
for P in 1 2 3 4 5 6; do rev mount-bln-pt$P.txt | cut -d "/" -f1 | rev | sort >> mount-bln-files-tmp.txt ; done
sort mount-bln-files-tmp.txt > mount-bln-files.txt
rm mount-bln-files-tmp.txt
wc -l mount-bln-files.txt
```
```
179669 mount-bln-files.txt
```

* Compare:

```bash
cmp bln-files.txt  mount-bln-files.txt
```

`cmp` should display nothing, indicating that the contents are the same.

---

## Copy Times Digital Archive dataset

Space required: ~362 GB

Mount CAHSS Digital Cultural Heritage DataStore directory into your home directory on Urika:

```bash
mkdir dch
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@chss.datastore.ed.ac.uk:/chss/datastore/chss/groups/Digital-Cultural-Heritage dch
```

Copy XML files only and set permissions in copy to be user-readable only:

```bash
nohup rsync -mrq --include "*/" --exclude "gale*.xml" --include "*.xml" --exclude "*" --chmod=Du=rwx,Dgo=,Fu=rwx,Fgo= dch/LBORO/TimesDigitalArchive_XMLS/TDA_GDA_1785-2009/ /mnt/lustre/<project>/<project>/<username>/TDA &
```

You can optionally validate the transfer as follows:

* Get file names in your local copy:

```bash
cd /mnt/lustre/<project>/<project>/<username>
find TDA/ -name "*.xml" > tda.txt
cut -d "/" -f4 tda.txt | sort > tda-files.txt
wc -l tda-files.txt
```
```
69699 tda-files.txt
```

* Get file names from DataStore:

```bash
find ~/dch/LBORO/TimesDigitalArchive_XMLS/TDA_GDA_1785-2009/ -name "*.xml" > mount-tda.txt 
cut -d "/" -f11 mount-tda.txt | grep -v gale | sort > mount-tda-files.txt
wc -l mount-tda-files.txt
```
```
69699 mount-tda-files.txt
```

* Compare:

```bash
cmp tda-files.txt mount-tda-files.txt
```

`cmp` should display nothing, indicating that the contents are the same.

---

## Copy Papers Past New Zealand and Pacific newspapers dataset

Space required: ~4 GB

Mount CAHSS Digital Cultural Heritage DataStore directory into your home directory on Urika:

```bash
mkdir dch
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@chss.datastore.ed.ac.uk:/chss/datastore/chss/groups/Digital-Cultural-Heritage dch
```

Copy XML files only and set permissions in copy to be user-readable only:

```bash
nohup rsync -mrq --include "*/" --include "*.xml" --exclude "*" --chmod=Du=rwx,Dgo=,Fu=rwx,Fgo= dch/LBORO/PP_XMLs\ \(via\ api\)/ /mnt/lustre/<project>/<project>/<username>/NZPP &
```

You can optionally validate the transfer as follows:

* Get file names in your local copy:

```bash
cd /mnt/lustre/<project>/<project>/<username>
find NZPP/ -name "*.xml" > nzpp.txt
cut -d "/" -f2 nzpp.txt | sort > nzpp-files.txt
wc -l nzpp-files.txt
```
```
13411 nzpp-files.txt
```

* Get file names from DataStore:

```bash
find ~/dch/LBORO/PP_XMLs\ \(via\ api\)/ -name "*xml" > mount-nzpp.txt
wc -l mount-nzpp.txt
cut -d "/" -f8 mount-nzpp.txt | sort > mount-nzpp-files.txt
```
```
13411 mount-nzpp-files.txt
```

* Compare:

```bash
cmp nzpp-files.txt  mount-nzpp-files.txt
```

`cmp` should display nothing, indicating that the contents are the same.
