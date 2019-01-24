#!/usr/bin/perl -w
use strict;

=pod
Usage perl after_prediction.pl af_pr_te.txt pr_test.txt > pred_amp_sequence_2.txt
af_pr_te.txt is the file created by predicted.py
pr_test.txt is the file created by translation.py
=cut

my $in = $ARGV[0]; 
open I, "<$in" || die "can`t open the file $in";
my ($a, @line_number);
my $i = 0;
while(defined($a =<I>)){
    chmod($a);
    $i++;
    if($a >= 0.99){ # this number is the predicted number, change it for high accuracy
        push(@line_number, $i)
        #print "$i\n";
    }
}
close I;

my $in1 = $ARGV[1]; # this file is the fasta sequence file after ORF_prediction
my ($b, %h);
my $j = 0;
open II,"<$in1" || die "can`t open the file $in1";
while(defined($b=<II>)){
    $b =~ s/\n//igm;
    $j++;
    $h{$j} = $b;
}
close II;

foreach my $number(@line_number){
        my $y = $number * 2;
        my $x = $y - 1;
        print "$h{$x}\n$h{$y}\n";
    }
