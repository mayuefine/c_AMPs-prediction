#!/usr/bin/python3
# -*- coding:utf-8 -*-
from keras.layers import Dense, Embedding, Conv1D, MaxPooling1D, LSTM, Dropout
from keras.models import Model, Sequential
from keras.preprocessing import sequence
from sklearn.model_selection import StratifiedKFold
from numpy import loadtxt, random, mean, std
from Metrics import Metric


# input data from local dataset
data_tr = loadtxt("/Users/mayue/Desktop/anti-data/data/tr.txt", delimiter=",")
x_tr = data_tr[:, 0:200]
y_tr = data_tr[:, -1]

print(len(x_tr), 'train sequences')
print('X_train shape:', x_tr.shape )

# created network model using keras
#embedding_vector_length = 128
nb_filter = 64
filter_length = 16
it = 20
seed = 10
random.seed(seed)

# 10 fold cross validation
kfold = StratifiedKFold(n_splits = 10, shuffle = True, random_state = seed)

cvscores = []
for train, test in kfold.split(x_tr, y_tr):

    met = Metric(it, validation_data = (x_tr[test],y_tr[test]))

    model = Sequential()
    model.add(Embedding(21, 128, input_length = 200))
    model.add(Conv1D(nb_filter, filter_length, strides = 1, activation = "relu"))
    model.add(MaxPooling1D(pool_size = 5, strides = 5))
    model.add(Dropout(0.1))
    model.add(LSTM(100, dropout = 0.1, unroll = True, stateful = False))
    model.add(Dense(1, activation = 'sigmoid'))
    model.compile(optimizer = "adam", loss = 'binary_crossentropy', metrics = ['accuracy'])

    print(model.summary())

    model.fit(x_tr[train], y_tr[train], validation_data = (x_tr[test],y_tr[test]), epochs = it, batch_size = 30, callbacks=[met])
    scores = model.evaluate(x_tr[test], y_tr[test],  verbose=0)

    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    
    cvscores.append(scores[1] * 100)

frp = []
frp.append(met.on_epoch_end(epoch = it))
tp = frp[0][3]
fp = frp[0][4]
tn = frp[0][5]
fn = frp[0][6]
acc = (tp+tn)/(tp+tn+fp+fn)
SENS = frp[0][1]
spec = tn/(tn+fp)
mcc = ((tp*tn)-(fn*fp))/(((tp+fn)*(tn+fp)*(tp+fp)*(tn+fn))**0.5)
roc = frp[0][7]

print("ACC: %.2f%%"%(acc*100))
print("Sensitivity: %.2f%%"%(SENS*100))
print("Specificity: %.2f%%"%(spec*100))
print("Accuracy: %.2f%%"%(scores[1]*100))
print("MCC: %.4f"%(mcc))
print("auROC: %.2f%%"%(roc*100))
print("ACC_STD: %.2f%% (+/- %.2f%%)" % (mean(cvscores), std(cvscores)))
model.save("test10cf.h5")
