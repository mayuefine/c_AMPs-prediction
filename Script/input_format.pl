#!/usr/bin/perl -w
use strict;

#### usage: perl format.pl AMP.te.fa 1 > amp.txt
#### 1 means true lable, 0 means false lable

my $in = $ARGV[0];
my $in1 = $ARGV[1];
my %aacode =
    (
    A => "1", C => "2", D => "3", E => "4",
    F => "5", G => "6", H => "7", I => "8",
    K => "9", L => "10", M => "11", N => "12",
    P => "13", Q => "14", R => "15", S => "16",
    T => "17", V => "18", W => "19", Y => "20",  X => "0",
    );
my ($a,$b);
open I,"<$in";
while(defined($a=<I>)){
    chomp($a);
    $a = uc $a;
    if($a =~ /\>/){
        $b = "0";
        }else{
        my @seq = split //,$a;
        my $len = @seq;
        my $i = 0;
        while($i < $len){
            $b = $b.",".$aacode{$seq[$i]};
            $i = $i + 1;
        }
        my @bb = split /,/, $b;
        my $lb = @bb;
        my $cha = 300 - $lb;
        my $j = 0;
        while($j < $cha){
            $b = "0".",".$b;
            $j = $j + 1;
        }
        if($in1 == 1){
            $b = $b.",1";
            print "$b\n";
        }elsif($in1 == 0){
            $b = $b.",0";
            print "$b\n";
        }
    }
}
close I;
