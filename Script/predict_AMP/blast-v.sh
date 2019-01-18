formatdb -i all_AMP.fa -p T
#-p means protein
blastp -query pred_amp_sequence_2.txt -db all_AMP.fa -out one_sample_test.txt -outfmt "6 qseqid sseqid pident length mismatch gaps qcovs" -max_target_seqs 1 -num_threads 8
# query.fa: prediction sequences
# db.fa: those we colleted AMPs sequences
