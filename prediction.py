#!/usr/bin/python3
# -*- coding:utf-8 -*-
from keras.models import load_model
from numpy import loadtxt, savetxt

model = load_model('test10cf.h5')
x = loadtxt("/Users/mayue/Downloads/Datasets_V2/non_amp_te.txt", delimiter=",")

preds = model.predict(x)
savetxt("/Users/mayue/Downloads/Datasets_V2/pr_non_amp.txt", preds, fmt="%.8f", delimiter=",")
