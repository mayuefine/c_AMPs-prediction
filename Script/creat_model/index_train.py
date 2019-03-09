#!/usr/bin/python3
# -*- coding:utf-8 -*-
from keras.models import load_model
from numpy import loadtxt, savetxt, arange, zeros, trapz, argmin
from Attention import Attention_layer
from keras import backend as K
import ROC

model = load_model('20f20b_10_0.9800_16.h5', custom_objects={'Attention_layer': Attention_layer})
x = loadtxt("x_train_16.txt", delimiter=",")
y = loadtxt("y_train_16.txt", delimiter=",")
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


#AP@k part
l_t = []
for i in arange(0, len(y)):
    if preds_x[i][0] >= 0.5:
        l_t.append([(preds_x[i][0], 1 + int(y[i]))])
    else:
        l_t.append([(preds_x[i][0], 0 + int(y[i]))])

s_l_t = sorted(l_t, reverse = True, key = lambda x:x[0])
del l_t[:]

def ap_at_k(number, sorted_list_t):
    ij = 0
    pr = []
    for j in arange(0, len(y)):
        if ij < number and sorted_list_t[j][0][1] == 2:
            ij = ij + 1
            pr.append(ij / (j+1))
        if ij >= number:
            break
    return sum(pr)/number, j

set_number = int(input("please input set number of AP@K: "))
if set_number >= len(y):
    print("The number you seted is bigger than %.0f, which is our total number of this test data, please reset it"%len(y))
    set_number = len(y)
apk = ap_at_k(set_number, s_l_t)

print("AP@K, K = %.0f: %.2f%%, and the last predition number is %.9f"%(set_number, apk[0]*100, s_l_t[apk[1]][0][0]))
print("Accuracy: %.2f%%"%(acc*100))
print("Sensitivity: %.2f%%"%(sens*100))
print("Specificity: %.2f%%"%(spec*100))
print("MCC: %.4f"%(mcc))
print("auROC: %.2f%%"%(auc*100))
print("Precision: %.2f%%"%(precision*100))
