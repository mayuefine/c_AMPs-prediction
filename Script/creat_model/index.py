#!/usr/bin/python3
# -*- coding:utf-8 -*-
from keras.models import load_model
from numpy import loadtxt, savetxt, ones, zeros
from Attention import Attention_layer
from keras import backend as K
import ROC

model = load_model('20f20b_100.97.h5', custom_objects={'Attention_layer': Attention_layer})
t = loadtxt("df_amp.txt", delimiter=",")
f = loadtxt("df_namp.txt", delimiter=",")
preds_t = model.predict(t).tolist()
preds_f = model.predict(f).tolist()

tp = 0
tn = 0
fp = 0
fn = 0
for i in preds_t:
    if i[0] >= 0.5:
        tp = tp + 1
    else:
        fn = fn + 1

for j in preds_f:
    if j[0] >= 0.5:
        fp = fp + 1
    else:
        tn = tn + 1

leng = len(preds_f)
preds_t.extend(preds_f)
lable = ones(leng)
lable = lable.tolist()
lable.extend(zeros(leng).tolist())
acc = (tp+tn)/(tp+tn+fp+fn)
sens = tp/(tp+fn)
spec = tn/(tn+fp)
precision = tp/(tp+fp)
mcc = ((tp*tn)-(fn*fp))/(((tp+fn)*(tn+fp)*(tp+fp)*(tn+fn))**0.5)
roc = ROC.roc_rate(preds_t, lable)

print("Accuracy: %.2f%%"%(acc*100))
print("Sensitivity: %.2f%%"%(sens*100))
print("Specificity: %.2f%%"%(spec*100))
print("MCC: %.4f"%(mcc))
print("auROC: %.2f%%"%(roc*100))
print("Precision: %.2f%%"%(precision*100))
