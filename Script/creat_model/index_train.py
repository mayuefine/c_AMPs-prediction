#!/usr/bin/python3
# -*- coding:utf-8 -*-
from keras.models import load_model
from numpy import loadtxt, savetxt, arange, zeros, trapz, argmin
from Attention import Attention_layer
from keras import backend as K
import ROC

model = load_model('20f20b_100.97.h5', custom_objects={'Attention_layer': Attention_layer})
x = loadtxt("x_train06.txt", delimiter=",")
y = loadtxt("y_train06.txt", delimiter=",")
preds_x = model.predict(x).tolist()

tp = 0
tn = 0
fp = 0
fn = 0
if len(y) == len(preds_x):
    for i in arange(0, len(y)):
        if preds_x[i][0] >= 0.5 and y[i] == 1:
            tp = tp + 1
        elif preds_x[i][0] < 0.5 and y[i] == 0:
            tn = tn + 1
        elif preds_x[i][0] >= 0.5 and y[i] == 0:
            fp = fp + 1
        elif preds_x[i][0] < 0.5 and y[i] == 1:
            fn = fn + 1

acc = (tp+tn)/(tp+tn+fp+fn+K.epsilon())
sens = tp/(tp+fn+K.epsilon())
spec = tn/(tn+fp+K.epsilon())
precision = tp/(tp+fp+K.epsilon())
mcc = ((tp*tn)-(fn*fp))/(((tp+fn)*(tn+fp)*(tp+fp)*(tn+fn))**0.5+K.epsilon())
auc = ROC.roc_rate(preds_x, y)

print("Accuracy: %.2f%%"%(acc*100))
print("Sensitivity: %.2f%%"%(sens*100))
print("Specificity: %.2f%%"%(spec*100))
print("MCC: %.4f"%(mcc))
print("auROC: %.2f%%"%(auc*100))
print("Precision: %.2f%%"%(precision*100))

