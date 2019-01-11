# Set up local environment

## Requirements

* [Apache Spark](https://spark.apache.org)
* Java 8
* Python 2.7

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
yum install java-1.8.0-openjdk-devel
wget https://repo.anaconda.com/archive/Anaconda2-5.1.0-Linux-x86_64.sh
```

### Install Anaconda 5.1 Python 2.7

For full information, see:

* Anaconda [Installation](https://docs.anaconda.com/anaconda/install/)
* [Download Anaconda Distribution](https://www.anaconda.com/download/)

After downloading installer, run:

```bash
bash Anaconda2-5.1.0-Linux-x86_64.sh
```

Create `anaconda2.sh` with content:

```bash
export PATH=/home/centos/anaconda2/bin:$PATH
```

Run:

```bash
source anaconda2.sh
pip install -r requirements.txt
```

### Install Apache Spark

For full information, see:

* [Spark Overview](https://spark.apache.org/docs/latest/index.html)
* [Download Apache Spark](https://spark.apache.org/downloads.html)

To quickly install, run:

```bash
wget http://apache.mirror.anlx.net/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.asc
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.md5
wget https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz.sha512
wget https://www.apache.org/dist/spark/KEYS
gpg --import KEYS
gpg --verify spark-2.3.0-bin-hadoop2.7.tgz.asc spark-2.3.0-bin-hadoop2.7.tgz
md5sum spark-2.3.0-bin-hadoop2.7.tgz
cat spark-2.3.0-bin-hadoop2.7.tgz.md5 
sha512sum spark-2.3.0-bin-hadoop2.7.tgz
cat spark-2.3.0-bin-hadoop2.7.tgz.sha512 
tar -xf spark-2.3.0-bin-hadoop2.7.tgz
cd spark-2.3.0-bin-hadoop2.7/
export PATH=~/spark-2.3.0-bin-hadoop2.7/bin:$PATH
```
