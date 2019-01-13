#!/usr/bin/perl -w
use strict;

=pod
Usage perl after_prediction.pl af_pr_te.txt pr_test.txt > predicted.fa.txt
af_pr_te.txt is the file created by predicted.py
pr_test.txt is the file created by translation.py
=cut

my $in = $ARGV[0]; 
my $in1 = $ARGV[1]; # this file is the fasta sequence file after ORF_prediction
open I, "<$in";
my ($a, @line_number);
my $i = 0;
while(defined($a =<I>)){
    chmod($a);
    $i++;
    if($a >= 0.99){ # this number is the predicted number, change it for high accuracy
        push(@line_number, $i)
    }
}
close I;
foreach my $number(@line_number){
    my $y = $number * 2;
    my $x = $y - 1;
    system("sed -n '$x,$y p' $in1"); # print put appointed fasta sqeuence with name
}
