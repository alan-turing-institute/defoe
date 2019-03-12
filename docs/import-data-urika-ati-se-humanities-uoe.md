# Import British Library Books and Newspapers data into Urika

**Note:** This information applies to Alan Turing Institute-Scottish Enterprise Data Engineering Program University of Edinburgh project members only.

## Mount British Library Books dataset

Mount dataset from DataStore into your home directory on Urika:

```bash
mkdir dch
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@chss.datastore.ed.ac.uk:/chss/datastore/chss/groups/Digital-Cultural-Heritage dch
```

Create directory on Lustre:

```bash
mkdir -p /mnt/lustre/<project>/<project>/<username>/BLB
```

Set file permissions so that no other user can access your data:

```bash
chmod -R go+rwx /mnt/lustre/<project>/<project>/<username>
```

Copy dataset to Lustre, by running in your home directory:

```bash
source scripts/copy_bl_books.sh ~/dch/BritishLibraryBooks/ /mnt/lustre/<project>/<project>/<username>/BLB
```

Set file permissions so you can read the data:

```bash
chmod -R u+rx /mnt/lustre/<project>/<project>/<username>/BLB/*/*.zip
```

## Mount British Library Newspapers dataset

Mount dataset from DataStore into your home directory on Urika:

```bash
mkdir blpaper
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@sg.datastore.ed.ac.uk:/sg/datastore/lib/groups/lac-store/blpaper blpaper
```

Create directory on Lustre:

```bash
mkdir -p /mnt/lustre/<project>/<project>/<username>/BLN
```

Set file permissions so that no other user can access your data:

```bash
chmod -R go+rwx /mnt/lustre/<project>/<project>/<username>
```

Copy dataset to Lustre, by running in your home directory:

```bash
source deploy/copy_bl_papers.sh ~/blpaper/xmls/ /mnt/lustre/<project>/<project>/<username>/BLN
```

Set file permissions so you can read the data:

```bash
chmod -R u+rx /mnt/lustre/<project>/<project>/<username>/BLN/*/*.xml
```

## Important

Do **not** mount DataStore directories directly onto Lustre.
