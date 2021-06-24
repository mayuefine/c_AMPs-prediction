#!/usr/bin/perl -w
## usage perl result.pl att_bact.txt lstm_bact.txt bert_bact.txt sequence.fa
use strict;
my $att = $ARGV[0];
my $lstm = $ARGV[1];
my $bert = $ARGV[2];
my $a;
my $l;
my $b;
my $i = 1;
my %h;
open ATT, "<$att";
while(defined($a=<ATT>)){
  $a =~ s/\s//igm;
  my $tmp;
  if($a > 0.5){
    $tmp = 1;
  }else{
    $tmp = 0;
  }
  $h{$i} = $tmp;
  $i++;
}
close ATT;

$i = 1;
open LSTM, "<$lstm";
while(defined($l=<LSTM>)){
  $l =~ s/\s//igm;
  my $tmp;
  if($l > 0.5){
    $tmp = 1;
  }else{
    $tmp = 0;
  }
  $h{$i} = $h{$i} + $tmp;
  $i++;
}
close LSTM;

$i = 1;
open BERT, "<$bert";
while(defined($b=<BERT>)){
  $b =~ s/\s//igm;
  my $tmp;
  if($b > 0.5){
    $tmp = 1;
  }else{
    $tmp = 0;
  }
  $h{$i} = $h{$i} + $tmp;
  $i++;
}
close BERT;

print "There are $i sequences need to predictive.\n";
print "name;size;AMP_prediction(1/0);\n";
my $seq = $ARGV[3];
my $se;
my $j = 1;
open SEQ, "<$seq";
while(defined($se=<SEQ>)){
  $se =~ s/\s//igm;
  if($se =~ />/){
    my $pr;
    if($h{$j} == 3){
      $pr = 1;
    }else{
      $pr = 0;
    }
    $se = $se.$pr;
    print "$se;\n";
    $j++;
  }else{
    print "$se\n";
  }
}
close SEQ;
