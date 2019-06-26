#!/usr/bin/env bash

/usr/bin/anaconda/bin/conda install --yes lxml
/usr/bin/anaconda/bin/conda install --yes nltk
/usr/bin/anaconda/bin/conda install --yes pep8
/usr/bin/anaconda/bin/conda install --yes pylint
/usr/bin/anaconda/bin/conda install --yes pycodestyle
/usr/bin/anaconda/bin/conda install --yes pytest
/usr/bin/anaconda/bin/conda install --yes PyYAML
/usr/bin/anaconda/bin/conda install --yes regex
/usr/bin/anaconda/bin/conda install --yes requests


/usr/bin/anaconda/bin/conda install --yes pip git
pip install git+https://github.com/alan-turing-institute/defoe.git
