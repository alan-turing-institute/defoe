# Set up Urika environment

## Get source code repository

Run:

```bash
git clone https://github.com/alan-turing-institute/defoe.git
```

This will clone the source code repository into a `defoe` directory.

---

## Set up Python environment

Create `urika-py27` environment:

```bash
module load anaconda3/4.1.1
conda create -n urika-py27 python=2.7 anaconda

Proceed ([y]/n)? y
```

Activate environment:

```bash
source activate urika-py27
```

Show active environment:

```bash
conda env list
```
```
...
urika-py27            *  /home/users/<your-urika-username>/.conda/envs/urika-py27
...
```

---

## Install dependencies

```bash
cd defoe
conda install -c anaconda --file requirements.txt
```

---

## Subsequent Urika sessions

After creating the `py27` environment, for your subsequent Urika sessions you just need to type:

```bash
module load anaconda3/4.1.1
source activate urika-py27
```
