#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
usage: python3 same_seq.py /Users/mayue/Desktop/anti-data/script/cnn_att_6.txt /Users/mayue/Desktop/anti-data/script/pred_amp_sequence_6.txt > same_amp.fa.txt
'''

from sys import argv

cnn_att = argv[1]
cnn_lstm = argv[2]

dic = {}
with open (cnn_att,"r") as file:
    for line in file:
        line = line.strip('\n')
        if line.startswith('>'):
            line = line.strip('>')
            key = line
        else:
            dic[key] = line

ke = []
with open (cnn_lstm,"r") as fil:
    for lin in fil:
        lin = lin.strip('\n')
        if lin.startswith('>'):
            lin = lin.strip('>')
            ke.append(lin)

for keys in ke:
    if keys in dic:
        print(">%s\n%s"%(keys, dic[keys]))
    else:
        pass