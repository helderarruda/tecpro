# python-template

<img src = "img/python-logo.png" width = "150"/>

Sugestão de cabeçalho padrão a ser utilizado em scripts Python que manipulam arquivos texto para uso com Machine Learning. Já traz algumas configurações de display que tornam mais prática a visualização de dados. Arquivo [python-template.py](python-template.py)

~~~ python
#!/usr/bin/env python
# coding=utf-8

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from __future__ import print_function
import sys, os
sys.path.append( os.path.expanduser( "~" ) + "/scripts" )
from __arruda__ import *
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
~~~

Importa o arquivo [\_\_arruda\_\_.py](../scripts/__arruda__.py), localizado no diretório [~/scripts](../scripts).

~~~ python
import pandas as pd
pd.options.display.width = None
pd.options.display.max_rows = 9

import numpy as np
np.set_printoptions( linewidth = None, threshold = 9 )

import scipy as sp

from sklearn import datasets
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
~~~
