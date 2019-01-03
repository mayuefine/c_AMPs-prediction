#!/usr/bin/python3
# -*- coding:utf-8 -*-
import numpy as np
from keras.callbacks import Callback
from keras import backend as K
from sklearn.metrics import f1_score, precision_score, recall_score, auc, roc_auc_score

class Metric(Callback):
    def __init__(self, steps, validation_data, verbose=0):
        self.steps = steps
        self.verbose = verbose
        self.validation_data = validation_data
        self.decay_steps = 5
        self.decay_rate = 0.90

    def on_train_begin(self, logs={}):
        self.val_f1s = []
        self.val_recalls = []
        self.val_precisions = []
        self.val_tp = []
        self.val_fp = []
        self.val_tn = []
        self.val_fn = []
        self.val_auroc = []
        self.lr = []

    def on_epoch_end(self, epoch, logs={}):
        y_predict = (np.asarray(self.model.predict(self.validation_data[0]))).round()
        y_p = (np.asarray(self.model.predict(self.validation_data[0])))
        y_true = self.validation_data[1]
        _val_f1 = f1_score(y_true, y_predict)
        _val_recall = recall_score(y_true, y_predict)
        _val_precision = precision_score(y_true, y_predict)
        (tp, fp, tn, fn) = self.performence(y_true, y_predict)
        _val_roc = roc_auc_score(y_true, y_p)
        self.val_f1s.append(_val_f1)
        self.val_recalls.append(_val_recall)
        self.val_precisions.append(_val_precision)
        self.val_tp.append(tp)
        self.val_fp.append(fp)
        self.val_tn.append(tn)
        self.val_fn.append(fn)
        self.val_auroc.append(_val_roc)
        #if epoch == 0:
            #K.set_value(self.model.optimizer.lr, 0.05)

        if epoch < self.steps and epoch % 2 == 0 and epoch != 0:
            self.lr = K.get_value(self.model.optimizer.lr)
            n_lr = self.lr * self.decay_rate ** (self.steps / self.decay_steps)
            self.change_lr(n_lr)
            print("Learning_Rate of last Epoch:", n_lr)
        '''
        old_lr = K.get_value(self.model.optimizer.lr)
        if epoch < self.steps:
            print("lr every time:", old_lr)
        n_lr = old_lr/4.8
        if epoch % 4 == 0 and epoch != 0:
            self.change_lr(n_lr)
        '''
        return self.val_f1s[-1], self.val_recalls[-1], self.val_precisions[-1], \
               self.val_tp[-1], self.val_fp[-1], self.val_tn[-1], self.val_fn[-1], self.val_auroc[-1]

    def performence(self, y_true, y_pred):
        not_y_pred = np.logical_not(y_pred) 
        y_int1 = y_true * y_pred 
        y_int0 = np.logical_not(y_true) * not_y_pred 
        tp = np.sum(y_pred*y_int1) 
        fp = np.sum(y_pred) - tp
        tn = np.sum(not_y_pred * y_int0) 
        fn = np.sum(not_y_pred) - tn
        return tp, fp, tn, fn

    def change_lr(self, new_lr):
        K.set_value(self.model.optimizer.lr, new_lr)
        if self.verbose == 1:
            print('Learning rate is %g' %new_lr)


''' |         1	                 |         0	              |         sum             |
1	| True Positive (TP)         | False Negative (FN)        | Actual Positive (TP+FN) |
0	| False Positive (FP)        | True Negative (TN)	      | Actual Negative (FP+TN) |
sum	| Predicted Positive (TP+FP) | Predicted Negative (FN+TN) |      TP+FP+FN+TN        |

fp = tn_fp - tn
fn = tp_fn - tp

SENS: TP/(TP + FN + K.epsilon()) x 100% = recall
SPEC: TN/(TN + FP + K.epsilon()) x 100%
ACC: (TP + TN)/(TP + FP + TN + FN + K.epsilon()) x 100%
Precision: TP/(TP + FP)
roc: TP/FP cruve
'''
