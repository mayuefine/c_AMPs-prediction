#!/usr/bin/perl -w
use strict;

=pod
Usage: perl after_blast.pl one_sample_test.txt pred_amp_sequence_2.txt
The file named short-test.txt was the file produced by blast-v.sh
and the q.fa is the file created by after_prediction.pl
=cut

my $in = $ARGV[0];
my ($a, @query, %delet);
open (I,"<$in") || die "can`t open the file $in";
while(defined($a=<I>)){
	chomp($a);
	my @sp = split /\t/, $a;
	$sp[0] =~ s/\s//igm;
	if($sp[2] >= 90 and $sp[-1] >= 90){
		$delet{$sp[0]} = 1;
	}else{
        push @query, $sp[0];
	}
}
close I;

my $i = 0;
my $len = @query;
for($i < $len){
	delete $query[$i] if($delet{$query[$i]} eq 1);
	$i++;
}
undef %delet;

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

my $output = "selected_sequence_90.fa.txt";
open OUT, ">>$output";
while(@query){
	my $selected_name = shift(@query);
	my $s_n = ">".$selected_name;
	print OUT "$s_n\n$h{$s_n}\n";
}
close OUT;
