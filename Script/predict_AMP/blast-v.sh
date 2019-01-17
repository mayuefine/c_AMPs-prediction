formatdb -i all_AMP.fa -p T
#-p means protein
blastp -query pred_amp_sequence_2.txt -db all_AMP.fa -out one_sample_test.txt -outfmt 6
# query.fa: prediction sequences
# db.fa: those we colleted AMPs sequences
# output file title are: query id, subject id, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
