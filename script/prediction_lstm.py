# -*- coding:utf-8 -*-

## usage python prediction_lstm.py sequence_after_format.txt lstm_bact.txt
from keras.models import load_model
from numpy import loadtxt, savetxt
from sys import argv

model = load_model('../Moldes/lstm.h5')
x = loadtxt(argv[1], delimiter=",")

preds = model.predict(x)
savetxt(argv[2], preds, fmt="%.8f", delimiter=",")
