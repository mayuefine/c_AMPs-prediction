#!/usr/bin/perl -w
use strict;

=pod
Usage: perl format.pl AMP.te.fa P > amp.txt
Here, P means positive true lable, N means negative false lable, and 
none means do not need using this function, using for predicted 
file re-format shuold silence this function
=cut

my $in = $ARGV[0];
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
        if($ARGV[1] eq "P" | $ARGV[1] eq "p"){
            $b = $b.",1";
            print "$b\n";
        }elsif($ARGV[1] eq "N" | $ARGV[1] eq "n"){
            $b = $b.",0";
            print "$b\n";
        }elsif($ARGV[1] eq "none"){
            print "$b\n";
        }
    }
}
close I;
