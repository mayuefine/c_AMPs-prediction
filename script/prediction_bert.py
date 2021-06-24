from os import environ
from sys import argv
# usage python prediction_bert.py sequences.fa proba.tsv
environ["CUDA_VISIBLE_DEVICES"] = "1"
seq_path = argv[1]

from bert_sklearn import BertClassifier
from bert_sklearn import load_model
 
import numpy as np
import pandas as pd

model = load_model("../Models/bert.bin")

tmp = pd.read_csv(seq_path, sep="\t", header=None, names=["seq"], index_col=False).seq.values
seq_array = []
for eachseq in tmp:
    if ">" not in eachseq:
        seq_array.append(" ".join(list(eachseq)))

seq_array = np.array(seq_array)

y_prob = model.predict_proba(seq_array)
y_prob = y_prob[:,1]
pd.DataFrame(y_prob).to_csv(argv[2], sep="\t", header=False, index=False)
