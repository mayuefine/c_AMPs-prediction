#!/usr/bin/python3
# -*- coding:utf-8 -*-

from re import match
from Bio.Seq import Seq

def orf(sequnce, table, min_pro_len, max_pro_len):
    seq = Seq(sequnce)
    #rs = s[::-1]
    #r_seq = Seq(rs) #(2, seq.complement()), (-1, r_seq),
    for strand, nuc in [(+1, seq),  (-2  , seq.reverse_complement())]:
        for frame in range(3):
            for pro in nuc[frame:].translate(table).split("*"):
                if max_pro_len >= len(pro) >= min_pro_len:
                    print(">length_%i\n%s" % (len(pro), pro[:]))
                    #print("%s,length_%i,strand_%i,frame_%i" % (pro[:], len(pro), strand, frame))

seqs = {}
fr = open("Assembly.scaftig") ## input scaftig file
for line in fr:
    if line.startswith('>'):
        name=line.split()[0]
        seqs[name]=''
    else:
        seqs[name]+=line.strip('\n')
fr.close()

wcsv = open('none.csv', 'w') # need move at last
for i in seqs.keys():
    wcsv.write(str(orf(seqs[i], 1, 5, 100)))
wcsv.close()
