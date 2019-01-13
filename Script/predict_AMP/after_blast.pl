#!/usr/bin/perl -w
use strict;

=pod
Usage: perl after_blast.pl short-test.txt q.fa
The file named short-test.txt was the file produced by blast-v.sh
and the q.fa is the file created by after_prediction.pl
=cut

#my $in = "/Users/mayue/Desktop/anti-data/script/short-test.txt";
my $in = $ARGV[0];
my ($a, @query);
open (I,"<$in") || die "can`t open the file $in";
print "query\tdata_base\n";
while(defined($a=<I>)){
	chomp($a);
	my @sp = split /\t/, $a;
	if($sp[2] >= 97 && $sp[-2] >= 90 && $sp[-1] >= 90){
		print "$sp[0]\t$sp[1]\n";
		$sp[0] =~ s/\s//igm;
        push @query, $sp[0];
	}
}
close I;

#my $in1 = "/Users/mayue/Desktop/anti-data/script/q.fa";
my $in1 = $ARGV[1];
my ($b, %h, $name);
open (IN,"<$in1") || die "can`t open the file $in";
while(defined($b=<IN>)){
	chomp($b);
	if($b =~ />/){
		$b =~ s/\s//igm;
		$name = $b;
	}else{
		$h{$name} = $b;
	}
}
close IN;

my $output = "selected_sequence.fa.txt";
open OUT, ">>$output";
while(@query){
	my $selected_name = shift(@query);
	my $s_n = ">".$selected_name;
	print OUT "$s_n\n$h{$s_n}\n";
}
close OUT;