#!/usr/bin/python3
# -*- coding:utf-8 -*-

from numpy import loadtxt, savetxt
from random import shuffle

data_tr = loadtxt("/Users/mayue/Desktop/anti-data/data/tr.txt", delimiter=",")
shuffle(data_tr)
savetxt("/Users/mayue/Desktop/anti-data/data/run_train.txt", data_tr, fmt="%.0f", delimiter=",")

#data_te = loadtxt("/Users/mayue/Downloads/Datasets_V2/te.txt", delimiter=",")
#shuffle(data_te)
#savetxt("/Users/mayue/Downloads/Datasets_V2/run_te.txt", data_te, fmt="%.0f", delimiter=",")
