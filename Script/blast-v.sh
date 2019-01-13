vsearch --usearch_global 1.fa -db q.fa --id 0.95 --threads 4 --strand both --maxaccepts 0 --maxrejects 0 --userout longer-test.txt --userfields query+target+id+alnlen+mism+opens+qcov+tcov
