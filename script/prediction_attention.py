# -*- coding:utf-8 -*-

## usage python prediction_attention.py bact.txt att_bact.txt
from keras.models import load_model
from numpy import loadtxt, savetxt
from Attention import Attention_layer
from sys import argv

model = load_model('../Models/att.h5', custom_objects={'Attention_layer': Attention_layer})
x = loadtxt(argv[1], delimiter=",")

preds = model.predict(x)
savetxt(argv[2], preds, fmt="%.8f", delimiter=",")
