# Set up Urika environment

## Set up Python environment

Create `py27` environment:

```bash
module load anaconda3/4.1.1
conda create -n py27 python=2.7 anaconda

Proceed ([y]/n)? y
```

Activate environment:

```bash
source activate py27
```

Show active environment:

```bash
conda env list
```
```
# conda environments:
#
py27                  *  /home/users/<your-urika-username>/.conda/envs/py27
root                     /opt/cray/anaconda3/4.1.1
```

Install dependencies:

```bash
cd i_newspaper_rods
conda install -c anaconda --file requirements.txt
```

**Note**:  After creating the `py27` environment, for your subsequent Urika sessions you just need to type:

```bash
module load anaconda3/4.1.1
source activate py27
```

---

## Mount datasets (University of Edinburgh users)

### British Library Books dataset

Mount dataset from DataStore into your home directory on Urika:

```bash
mkdir dch
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@chss.datastore.ed.ac.uk:/chss/datastore/chss/groups/Digital-Cultural-Heritage dch
```

Create directory on Lustre:

```bash
mkdir -p /mnt/lustre/<your-urika-username>/dch
```

Copy dataset to Lustre, by running in your home directory:

```bash
source scripts/copy_bl_books.sh ~/dch/BritishLibraryBooks/ /mnt/lustre/<username>/dch/BritishLibraryBooks
```

Set file permissions:

```bash
chmod -R u+rx /mnt/lustre/<your-urika-username>/dch/*/*.zip
```

### British Library dataset

Mount dataset from DataStore into your home directory on Urika:

```bash
mkdir blpaper
sshfs -o intr,large_read,auto_cache,workaround=all -oPort=22222 <your-datastore-username>@sg.datastore.ed.ac.uk:/sg/datastore/lib/groups/lac-store/blpaper blpaper
```

Create directory on Lustre:

```bash
mkdir -p /mnt/lustre/<your-urika-username>/blpaper/xmls
```

Copy dataset to Lustre, by running in your home directory:

```bash
source deploy/copy_bl_papers.sh ~/blpaper/xmls/ /mnt/lustre/<your-urika-username>/blpaper/xmls
```

Set file permissions:

```bash
chmod -R u+rx /mnt/lustre/<your-urika-username>/blpaper/*/*.xml
```

### Important

Do **not** mount DataStore directories directly onto Lustre. Urika compute nodes have no network access and so cannot access DataStore via the mount. Also, for efficient processing, data movement needs to be minimised

Copy the data into Lustre!
