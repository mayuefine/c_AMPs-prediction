#!/usr/bin/python3
# -*- coding:utf-8 -*-

#### usage : python3 translation.py > prediction_sequences.fa.txt

from Bio.Seq import Seq

def orf(sequnce, table, min_pro_len, max_pro_len, scaftig_sequence_name):
    seq = Seq(sequnce)
    number = 1
    for strand, nuc in [(+1, seq),  (-2, seq.reverse_complement())]:
        for frame in range(3):
            for pro in nuc[frame:].translate(table).split("*"):
                if max_pro_len >= len(pro) >= min_pro_len:
                    print(">prediction_%s_%i\n%s" % (scaftig_sequence_name.replace('>',''), number, pro[:]))
                    number = number + 1
                    #print("%s,length_%i,strand_%i,frame_%i" % (pro[:], len(pro), strand, frame))

seqs = {}
fr = open("AAssembly.scaftig")
for line in fr:
    if line.startswith('>'):
        name=line.split()[0]
        seqs[name]=''
    else:
        seqs[name]+=line.strip('\n')
fr.close()

for i in seqs.keys():
    str(orf(seqs[i], 1, 5, 100, i))
