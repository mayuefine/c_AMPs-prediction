#!/usr/bin/python3
# -*- coding:utf-8 -*-
from keras.models import load_model
from numpy import loadtxt, savetxt, ones, zeros, arange
from Attention import Attention_layer
from keras import backend as K
import ROC

model = load_model('20f20b_10_0.9800_16.h5', custom_objects={'Attention_layer': Attention_layer})
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


# data format part
t_l = ones(leng)
f_l = zeros(leng)
y = t_l.tolist()
y.extend(f_l.tolist())
preds_x = preds_t

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
print("auROC: %.2f%%"%(roc*100))
print("Precision: %.2f%%"%(precision*100))
