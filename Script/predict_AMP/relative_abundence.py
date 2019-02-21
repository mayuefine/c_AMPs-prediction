#!/usr/bin/python3
# -*- coding:utf-8 -*-

'''
usage: python3 relative_abundence.py /Users/mayue/Desktop/blast_reslut.txt /Users/mayue/Desktop/sequences_name.txt > amp_relative_abundence.txt
'''

from sys import argv

blast_reslut = argv[1]
seq_name = argv[2]

dic = {}
with open (blast_reslut,"r") as file:
	for line in file:
		line = line.strip('\n')
		a = line.split('\t')
		f1 = a[0]
		r1 = a[1]
		num = float(a[2])
		if f1 != r1 and 90 <= num <= 100:
			#print(line)
			if f1 >= r1:
				dic.setdefault(f1, []).append(r1)
			else:
				dic.setdefault(r1, []).append(f1)

k = []
for key in dic:
	k.append(key)

kj_name = []
for ki in k:
	for kj in k:
		if kj in dic[ki]:
			dic[ki] = dic[ki] + dic[kj]
			kj_name.append(kj)

kj_name = list(set(kj_name))
for i in kj_name:
	if i not in k:
		print(i)
	else:
		k.remove(i)
del kj_name[:]

cluster = []
clus = {}
for keys in k:
	temp = dic[keys][:]
	temp = list(set(temp))
	cluster.append(keys)
	cluster = cluster + temp
	clus[keys] = len(temp) + 1
	#print(keys, ':', len(temp) + 1)
del dic
del k[:]

diction ={}
with open (seq_name,"r") as fil:
	for lin in fil:
		lin = lin.strip('>')
		lin = lin.strip('\n')
		#print(lin)
		diction[lin] = 1

for it in cluster:
	if diction[it]:
		diction[it] += 1
del cluster[:]

for key_i in diction:
	if diction[key_i] == 1:
		print(key_i, ':', 1)
del diction

for k_key in clus:
	print(k_key, ':', clus[k_key])
