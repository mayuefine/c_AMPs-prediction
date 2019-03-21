formatdb -i all_AMP.fa -p T
#-p means protein
blastp -query pred_amp_sequence_2.txt -db all_AMP.fa -out one_sample_test.txt -outfmt "6 qseqid sseqid pident length mismatch gaps qcovs" -max_target_seqs 1 -num_threads 8
# query.fa: prediction sequences, this file is coming from after_prediction.pl script
# db.fa: those we colleted AMPs sequences


# or can try diamond to accelerate alignment process
diamond makedb --in pred_amp_sequence_2.txt -d reab_test
diamond blastp -d reab_test -q pred_amp_sequence_2.txt -o test.fa -f 6
# output file format is blast 6 format, each column head description as below:
# 1.	 qseqid	 query (e.g., gene) sequence id
# 2.	 sseqid	 subject (e.g., reference genome) sequence id
# 3.	 pident	 percentage of identical matches
# 4.	 length	 alignment length
# 5.	 mismatch	 number of mismatches
# 6.	 gapopen	 number of gap openings
# 7.	 qstart	 start of alignment in query
# 8.	 qend	 end of alignment in query
# 9.	 sstart	 start of alignment in subject
# 10.	 send	 end of alignment in subject
# 11.	 evalue	 expect value
# 12.	 bitscore	 bit score
