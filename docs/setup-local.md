# Set up local environment

## Requirements

* [Apache Spark](https://spark.apache.org)
* Java 8
* Python 2.7

---

## Get source code repository

Run:

```bash
git clone https://github.com/alan-turing-institute/defoe.git
```

This will clone the source code repository into a `defoe` directory.

---

## Set up Mac OS X

Run:

```bash
brew install apache-spark
```

---

## Set up CentOS 7

### Install Java 1.8

Run:

```bash
yum install -y java-1.8.0-openjdk-devel
```

### Install Anaconda Python 2.7

For full information, see:

* Anaconda [Installation](https://docs.anaconda.com/anaconda/install/)
* [Download Anaconda Distribution](https://www.anaconda.com/download/)

For example:

```bash
wget https://repo.continuum.io/archive/Anaconda2-2018.12-Linux-x86_64.sh
```

After downloading installer, run:

```bash
bash Anaconda2-2018.12-Linux-x86_64.sh
```

Create `setenv-py2.sh`:

```bash
echo 'export PATH=$HOME/anaconda2/bin:$PATH' > setenv-py2.sh
echo 'source $HOME/anaconda2/etc/profile.d/conda.sh' >> setenv-py2.sh
```

Run:

```bash
source setenv-py2.sh
python -V
```
```
Python 2.7.15 :: Anaconda, Inc.
```

### Install Apache Spark

For full information, see:

* [Spark Overview](https://spark.apache.org/docs/latest/index.html)
* [Download Apache Spark](https://spark.apache.org/downloads.html)

To quickly install, download package, signatures, checksums, keys:

```bash
wget http://apache.mirror.anlx.net/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz

wget https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz.asc
wget https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz.sha512

wget https://www.apache.org/dist/spark/KEYS
```

Validate signatures, checksums, keys:

```bash
gpg --import KEYS
gpg --verify spark-2.4.0-bin-hadoop2.7.tgz.asc spark-2.4.0-bin-hadoop2.7.tgz
```
```
gpg: Signature made Mon 29 Oct 2018 06:36:32 GMT using RSA key ID 4F4FDC8A
gpg: Good signature from "Wenchen Fan (CODE SIGNING KEY) <wenchen@apache.org>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 9B31 1CB5 38F2 1588 6143  5661 6BAC 7289 4F4F DC8A
```
```bash
gpg --fingerprint 4F4FDC8A
```
```
pub   4096R/4F4FDC8A 2018-09-18
      Key fingerprint = 9B31 1CB5 38F2 1588 6143  5661 6BAC 7289 4F4F DC8A
uid                  Wenchen Fan (CODE SIGNING KEY) <wenchen@apache.org>
sub   4096R/6F3F5B0E 2018-09-18
```
```bash
sha512sum spark-2.4.0-bin-hadoop2.7.tgz
cat spark-2.4.0-bin-hadoop2.7.tgz.sha512
```

Unpack:

```bash
tar -xf spark-2.4.0-bin-hadoop2.7.tgz
echo 'export PATH=$HOME/spark-2.4.0-bin-hadoop2.7/bin:$PATH' >> setenv-py2.sh
export PATH=~/spark-2.4.0-bin-hadoop2.7/bin:$PATH
```

### Install dependencies

Ins
```bash
cd defoe
conda install -c anaconda --file requirements.txt 
pip freeze | grep azure > azure.txt
pip uninstall -y -r azure.txt
rm azure.txt
conda install -c conda-forge azure
```

### Install NLTK data

Certain queries require the NLTK corpora data to be installed.

```bash
bash scripts/download_ntlk_corpus.sh
```

This is installed to `<HOME>/nltk_data`

**Caution:** the NLTK data requires ~3GB of space.

For more information, see [Installing NLTK Data](https://www.nltk.org/data.html)
