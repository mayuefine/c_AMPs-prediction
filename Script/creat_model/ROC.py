#!/usr/bin/python3
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from keras import backend as K

def cal_rate(pred, lable, thres):
    all_number = len(pred)
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for item in np.arange(0, len(lable)):
        if pred[item][0] >= thres[0] and lable[item] == 1:
            TP = TP + 1
        elif pred[item][0] < thres[0] and lable[item] == 0:
            TN = TN + 1
        elif pred[item][0] >= thres[0] and lable[item] == 0:
            FP = FP + 1
        elif pred[item][0] < thres[0] and lable[item] == 1:
            FN = FN + 1
    TPR = float(TP) / float(TP + FN + K.epsilon())
    TNR = float(TN) / float(FP + TN + K.epsilon())
    FNR = float(FN) / float(TP + FN + K.epsilon())
    FPR = float(FP) / float(FP + TN + K.epsilon())
    return TPR, TNR, FNR, FPR

def roc_rate(pred, lable):
    threshold_vaule = sorted(pred)
    threshold_num = len(threshold_vaule)
    TPR_array = np.zeros(threshold_num)
    TNR_array = np.zeros(threshold_num)
    FNR_array = np.zeros(threshold_num)
    FPR_array = np.zeros(threshold_num)

    for thres in range(threshold_num):
        TPR, TNR, FNR, FPR = cal_rate(pred, lable, threshold_vaule[thres])
        TPR_array[thres] = TPR
        TNR_array[thres] = TNR
        FNR_array[thres] = FNR
        FPR_array[thres] = FPR

    AUC = np.trapz(TPR_array, FPR_array)
    threshold = np.argmin(abs(FNR_array - FPR_array))
    EER = (FNR_array[threshold] + FPR_array[threshold]) / 2
    plt.plot(FPR_array, TPR_array)
    plt.title('ROC')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    #plt.show()
    plt.savefig('roc.png')
    return -AUC
