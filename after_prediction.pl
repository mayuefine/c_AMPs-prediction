#!/usr/bin/perl -w
use strict;

#### usage perl after_prediction.pl af_pr_te.txt pr_test.txt > predicted.fa.txt

my $in = $ARGV[0]; # this file contain numbers after perdiction function
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
