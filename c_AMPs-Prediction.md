# Candidate AMPs Prediction Process
---

## Contents
__1. Get small orf;__
__2. Remove same small orfs;__
__3. AMP prediction;__ 
__4. Protein potential ;__
__4.1 Optional section: get selected c_AMPs names ;__
__5. Network analysis between c_AMPs and bacteria;__

---
## Scripts
### 1. Prediction small ORF from genome sequences
  - Here we using perl script to do multiply small ORF predicted.
    ```perl{.line-numbers}
       #!/usr/bin/perl -w
       use strict;
       my $in = "fasta_sequence_names";
       my ($a, $cmd);
       open I, "<$in";
       while(defined($a=<I>)){
           $a =~ s/\n//igm;
           my $out_name = $a.".orf.fa"; 
           $cmd = "getorf -sequence /fasta_sequence_path/".$a." -find 1 -table 11 -minsize 15 -maxsize 150 -outseq /output_sequnces_path/".$out_name;
           system("$cmd");
           #print "$cmd\n"; # print command to screen before real execute
       }
       close I;
    ```
  - fasta_sequence_names should look like this:
    ```bash{.line-numbers}
      head -5 fasta_sequence_names
      family_Acetobacteraceae_otu1.fa
      family_Acetobacteraceae_otu2.fa
      family_Acetobacteraceae_otu3.fa
      family_Acetobacteraceae_otu4.fa
      family_Acetobacteraceae_otu5.fa
    ```
---
### 2. Remove the redundant sORF and known AMPs
  - Merge all orf.fa to one orf fasta file
    ```bash{.line-numbers}
       cat *.fa > ../all_orf.fa
    ```
  - Using perl script to remove redundant sORF and known AMPs:
    ```perl{.line-numbers}
       #!/usr/bin/perl -w
       use strict;
       my $in = "all_orf.fa";
       my $a;
       my %h;
       my $name;
       open I,"<$in";
       while(defined($a=<I>)){
           $a =~ s/\n//igm;
           if($a =~ />/){
               $a =~ s/\s/_/igm;
               $name = $a;
           }else{
               $a =~ s/\s//igm;
               $h{$a} = $name."\n".$a;
           }
       }
       close I;

       my $in1 = "kown_AMP.fa";
       my $b;
       open II,"<$in1";
       while(defined($b=<II>)){
           $b =~ s/\n//igm;
           if($b =~ />/){
           }else{
               $b =~ s/\s//igm;
               if($h{$b}){
                   $h{$b} = "AMP";
               }
           }
       }
       close II;

       foreach my $k (keys %h){
           if($h{$k} eq "AMP"){ # Change eq with ne you can get kown AMP sequence as output
           }else{
               print "$h{$k}\n";
           }
       }
    ```
---
### 3. AMP prediction parts
  - Prepare three prediction models 
    ```bash{.line-numbers}
      Attention model => 10att.h5
      LSTM model => 10lstm.h5
      BERT model => bert.bin
    ```
  - Prepare input data format for LSTM and Attention models
    ```perl{.line-numbers}
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
           T => "17", V => "18", W => "19", Y => "20",
           );
       my ($a,$b);
       open I,"<$in";
       while(defined($a=<I>)){
           chomp($a);
           $a = uc $a;
           if($a =~ /\>/){
               $b = "0";
               }else{
               if($a =~ /B/){}
               elsif($a =~ /J/){}
               elsif($a =~ /O/){}
               elsif($a =~ /U/){}
               elsif($a =~ /X/){}
               elsif($a =~ /Z/){}
               else{
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
       }
       close I;
    ```
  - Attention Model;
    ```python{.line-numbers}
       ## usage python3 prediction_10att.py bact.txt 10att_bact.txt
       from keras.models import load_model
       from numpy import loadtxt, savetxt
       from Attention import Attention_layer
       from sys import argv

       model = load_model('10att.h5', custom_objects={'Attention_layer': Attention_layer})
       x = loadtxt(argv[1], delimiter=",")

       preds = model.predict(x)
       savetxt(argv[2], preds, fmt="%.8f", delimiter=",")
    ```
  - Attention_layer from Attention.py;
    ```python{.line-numbers}
       # -*- coding:utf-8 -*-
       from keras import backend as K
       from keras.engine.topology import Layer
       from keras import initializers, regularizers, constraints

       class Attention_layer(Layer):
           def __init__(self,
                        W_regularizer=None, b_regularizer=None,
                        W_constraint=None, b_constraint=None,
                        bias=True, **kwargs):
               self.supports_masking = True
               self.init = initializers.get('glorot_uniform')
               self.W_regularizer = regularizers.get(W_regularizer)
               self.b_regularizer = regularizers.get(b_regularizer)
               self.W_constraint = constraints.get(W_constraint)
               self.b_constraint = constraints.get(b_constraint)
               self.bias = bias
               super(Attention_layer, self).__init__(**kwargs)

           def build(self, input_shape):
               assert len(input_shape) == 3
               self.W = self.add_weight((input_shape[-1], input_shape[-1],),
                                        initializer=self.init,
                                        name='{}_W'.format(self.name),
                                        regularizer=self.W_regularizer,
                                        constraint=self.W_constraint)
               if self.bias:
                   self.b = self.add_weight((input_shape[-1],),
                                            initializer='zero',
                                            name='{}_b'.format(self.name),
                                            regularizer=self.b_regularizer,
                                            constraint=self.b_constraint)
 
               super(Attention_layer, self).build(input_shape)

           def compute_mask(self, input, input_mask=None):
               return None

           def call(self, x, mask=None):
               uit = K.dot(x, self.W)

               if self.bias:
                   uit += self.b

               uit = K.tanh(uit)
               a = K.exp(uit)
               if mask is not None:
                   a *= K.cast(mask, K.floatx())
               a /= K.cast(K.sum(a, axis=1, keepdims=True) + K.epsilon(), K.floatx())
               print(a)
               print(x)
               weighted_input = x * a
               print(weighted_input)
               return K.sum(weighted_input, axis=1)

           def compute_output_shape(self, input_shape):
               return (input_shape[0], input_shape[-1])
    ```
  - LSTM Models；
    ```python{.line-numbers}
      ## usage python3 prediction_10lstm.py bact.txt 10lstm_bact.txt
      from keras.models import load_model
      from numpy import loadtxt, savetxt
      from sys import argv

      model = load_model('10lstm.h5')
      x = loadtxt(argv[1], delimiter=",")

      preds = model.predict(x)
      savetxt(argv[2], preds, fmt="%.8f", delimiter=",")
    ```
  - BERT Model;
    ```python{.line-numbers}
        from os import environ
        from sys import argv
        # usage python prediction_bert.py EUK_PEP_DB_drp.fa EUK.proba.tsv
        environ["CUDA_VISIBLE_DEVICES"] = "1"
        seq_path = argv[1]
        from bert_sklearn import BertClassifier
        from bert_sklearn import load_model
        import numpy as np
        import pandas as pd
        model = load_model("bert.bin")
        tmp = pd.read_csv(seq_path, sep="\t", header=None, names=["seq"], index_col=False).seq.values
        seq_array = []
        for eachseq in tmp:
            if ">" not in eachseq:
                seq_array.append(" ".join(list(eachseq)))

        seq_array = np.array(seq_array)
        y_prob = model.predict_proba(seq_array)
        y_prob = y_prob[:,1]
        pd.DataFrame(y_prob).to_csv(argv[2], sep="\t", header=False, index=False)
     ```
  - Result integration
     ```perl{.line-numbers}
        #!/usr/bin/perl -w
        use strict;
        my $att = "10att_bact.txt"; # result from attention model prediction
        my $lstm = "10lstm_bact.txt"; # result from LSTM model prediction
        my $bert = "bert_bact.txt"; # result from BERT model prediction
        my $seq = "sequences_using_for_AMP_prediction.fa";
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
        my $se;
        my %sequence;
        my $seq_name;
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
            $se = $se."|".$pr;
            $seq_name = $se;
            $j++;
          }else{
            $sequence{$seq_name} = $se;
          }
        }
        close SEQ;

        foreach my $k (keys %sequence){
            if($k =~ /\|1/){ # 1 means sequences with AMP activate，change $k =~ /\|1/ to $k =~ /\|/ will output all sequences with prediction values.
                print "$k\n$sequence{$k}\n";
            }
        }
     ```
  - The number 1 after sequences name means this sequence with AMP activty, 0 means non AMP.
  - Output like this；
     ```bash{.line-numbers}
        There are 762218 sequences need to predictive.
        name;size;AMP_prediction(1/0);
        >11U203_Scaf9_1553_[51637_-_51705]_|1
        MFLFKPFCLSLYLSSSYHFKIVT
        >17R251_Scaf10_2205_[28547_-_28530]_(REVERSE_SENSE)_|1
        MRFVVK
    ```
---
### 4. Candidate AMPs which with protein potential will be selected in this section;
  - Selected length smaller than 50 AA proteom sequences
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      # perl count.pl all_seq.fa > less_50_data.fa
      use strict;
      my $in = $ARGV[0];
      my $a;
      my $temp = "";
      open I,"<$in";
      while(defined($a=<I>)){
        $a =~ s/\n//gm;
        $a =~ s/\s/_/gm;
        if($a =~ />/){
          $temp = $a;    
        }else{
          my @len = split //, $a;
          my $le = @len;
          if(4 < $le && $le < 51){
            if($temp){
              print"$temp\n$a\n";
            }else{
              print "$a\n";
            }
          }
        }
      }
      close I; 
    ```
  - Transformation of c_AMPs sequences into fragments of a certain length, here we setting the length were contain from full length to half length;
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      use strict;
      # usage perl kmer.pl Sequence.fa > mers.fa

      my $in = $ARGV[0]; # Sequence.fa from "Result integration" section, and remove 2 head line. 
      my $b;
      my %h;
      open I,"<$in";
      while(defined($b=<I>)){
          $b =~ s/\n//igm;
          $b =~ s/\s//igm;
          $b =~ s/\*//igm;
          if($b =~ />/){}else{
              my @pr = &kmer($b);
              my $mers = join(',',@pr);
              print "$b:$mers\n";
          }
      }
      close I;

      sub kmer{
          (my $sequ) = @_;
          my @a = split //, $sequ;
          my $le = @a;
          my $len = int($le/2)-1;
          my $ii = 0;
          my @se;
          while($ii < $le){
             my $leng_set = $len;
             while($leng_set <= $le){
                 if($ii+$leng_set < $le){
                     my $temp = join('',@a[$ii..$leng_set+$ii]);
                     push @se, $temp;
                 }
                 $leng_set++;
             }
             $ii++;
          }
      return @se;
      }
    ```
  - Set mers.fa to dictionary data format and every single mers from c_AMPs were setted as dictionary keys, the original c_AMPs were dictionary values.
  - If the mers.fa over 2GB, you shuold split it to small files. Otherwise this script will cause system core dump :/, which will decide by your system memory (RAM) size.
    ```bash{.line-numbers}
      split -1000 mers.fa
    ```
  - Key => value format;
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      use strict;
      # usage perl k_mer_dict.pl xaa key_values_01

      my $in = $ARGV[0];
      my $b;
      my %h;
      my $b1;
      open I,"<$in";
      while(defined($b=<I>)){
          $b =~ s/\n//igm;
          $b =~ s/(?<se>.*:)(?<k>.*)//igm;
          $b1 = $+{se};
          my $pp = $+{k};
          my @pr = split /,/, $pp;
          $b1 =~ s/://igm;
          dic1(@pr,$b1);
      }
      close I;

      sub dic1{
          (my @ks) = @_;
          my $va = $b1;
          foreach my $kk (@ks){
              $h{$kk}{$va} = 1;
          }
      }

      foreach my $ke (keys %h){
          my $h2 = $h{$ke};
          my $k2 = join(',',keys %$h2);
          print "$ke: ", $k2,"\n";
      }
    ```
  - Selected the c_AMPs that appears in the proteome;
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      use strict;
      # usage perl run.pl key_values_01 proteom_less_50.fa key_values_01.out

      my $in = $ARGV[0];
      my $b;
      my %h;
      open I,"<$in";
      while(defined($b=<I>)){
          $b =~ s/\n//igm;
          $b =~ s/(?<se>.*:)(?<k>.*)//igm;
          my $b1 = $+{se};
          my $pp = $+{k};
          $b1 =~ s/\s//igm;
          $b1 =~ s/://igm;
          $pp =~ s/\s//igm;
          $h{$b1} = $pp;
      }
      close I;

      my $in1 = $ARGV[1];
      my $a;
      open II,"<$in1";
      while(defined($a=<II>)){
          $a =~ s/\n//igm;
          $a =~ s/\s//igm;
          $a =~ s/\*//igm;
          if($a =~ />/){}else{
              if($h{$a}){
                  print"$a:$h{$a}\n";
              }
          }
      }
      close II;
    ```
  - Merge all *.out file to one file
    ```bash{.line-numbers}
      cat *.out > selected_c_AMPs_out.txt
    ```
  - Formatting output sequences
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      use strict;
      # usage perl selec_seq_frmt.pl selected_c_AMPs_out.txt > selected_c_AMPs.fa

      my $a;
      my %h;
      my $i = 1;
      open I,"<$ARGV[0]";
      while(defined($a=<I>)){
          chomp($a);
          my @aa = split(/:/, $a);
          my $pp = $aa[1];
          $pp =~ s/,/\n/igm;
          $h{$pp} = ">c_APM".$i;
          $i++;
      }
      close I;

      foreach my $k (keys %h){
          print "$h{$k}\n$k\n";
      }
    ```
---
### 4.1 This section were optional
  - Get selected c_AMPs sequences name (the names, if this sORF were get from different genome sequences ) from sORF sequece;
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      use strict;
      # usage perl get_orf_names.pl all_orf.fa selected_c_AMPs.fa > selected_c_AMPs_genome_names.fa

      my $a;
      my %h;
      my $seq_name;

      open I,"<$ARGV[0]";
      while(defined($a=<I>)){
          chomp($a);
          if($a =~ />/){
              $a =~ s/>//igm;
              $a =~ s/\s/_/igm;
              $seq_name = $a;
          }elsif($h{$a}){
              $h{$a} .= ",SEQ:".$seq_name;
          }else{
              $h{$a} = ">".$seq_name;
          }
      }
      close I;

      my $b;
      open II, "<$ARGV[1]";
      while(defined($b=<II>)){
          chomp($b);
          $b =~ s/\s//igm;
          if($b =~ />/){
          }else{
              print "$h{$b}\n$b\n";
          }
      }
      close II;
    ```
  - Get selected c_AMPs sequences name from proteom sequece; :)
    ```perl{.line-numbers}
      #!/usr/bin/perl -w
      use strict;
      # usage perl get_proteom_names.pl selected_c_AMPs_out.txt proteom_less_50.fa > selected_c_AMPs_proteom_names.fa

      my $b;
      my %h;
      my $seq_name;
      open II, "<$ARGV[1]";
      while(defined($b=<II>)){
          chomp($b);
          if($b =~ />/){
              $b =~ s/>//igm;
              $b =~ s/\s/_/igm;
              $seq_name = $b;
          }elsif($h{$b}){
              $h{$b} .= ",SEQ:".$seq_name;
          }else{
              $h{$b} = ">".$seq_name;
          }
      }
      close II;

      my $a;
      open I,"<$ARGV[0]";
      while(defined($a=<I>)){
          chomp($a);
          my @aa = split(/:/, $a);
          my $pp = $aa[0];
          $pp =~ s/\s//igm;
          print "$h{$pp}\n$pp\n";
      }
      close I;
    ```
---
### 5. Network analysis between AMPs and bacteria
  - Befor network analysis, we need caculated relative abundence of c_AMPs;
    - install software;
    ```bash{.line-numbers}
      wget https://sourceforge.net/projects/samtools/files/samtools/1.7/samtools-1.7.tar.bz2/download -O samtools-1.7.tar.bz2
      wget https://sourceforge.net/projects/samtools/files/samtools/1.7/htslib-1.7.tar.bz2/download -O htslib-1.7.tar.bz2
      tar jxvf htslib-1.7.tar.bz2
      tar jxvf samtools-1.7.tar.bz2

      # Cenos, root
      yum -y install bzip2-devel
      yum -y install ncurses-libs
      yum -y install ncurses-devel 
      yum -y install xz-devel.x86_64
      yum -y install zlib-devel
      yum -y install curl-devel
      yum -y install git
      
      # Ubuntu, root
      apt-get install libbz2-dev
      apt-get install zlib1g-dev
      apt-get install liblzma-dev
      apt-get install libncurses5-dev
      apt-get install libcurl4-openssl-dev

      git clone https://github.com/twestbrookunh/paladin.git
      cd paladin/
      make
      PATH=$PATH:$(pwd)


      cd htslib-1.7
      ./configure
      make
      make install

      cd samtools-1.7
      make clean
      make
      make prefix=/opt/samtools install
      echo 'export PATH=$PATH:/opt/samtools/bin' >> /etc/profile
      source /etc/profile
    ```
    - Abundence caculation
    ```bash{.line-numbers}
      # Create index
      paladin index -r3 selected_c_AMPs.fa 

      # Compare to generate bam files. Takes the most time.
      paladin align -t 4 selected_c_AMPs.fa test.fa | samtools view -Sb - > t1.bam

      # Apply samtools to get the comparison file, re_ab.csv is the abundance of c_AMPs
      samtools sort t1.bam -o s1.bam
      samtools index s1.bam
      samtools idxstats s1.bam >> re_ab.csv
    ```
  - Relative abundence caculation
    ```R{.line-numbers}
      # integration part
      name <- read.csv("name.csv", header = F) # name.csv contain re_ab.csv for each line
      n <- nrow(name)
      na <- t(name)
      result <- c(0)
      for(i in 1:n){
        data <- read.csv(as.character(name[i,]), header = F, sep = '\t')
        data <- data[-nrow(data),]
        result <- cbind(result, data[,3])
      }
      result <- as.data.frame(result)
      result$result <- data[,1]
      na <- cbind('Sample', na)
      colnames(result) <- na
      # 0.05 part
      nr <- nrow(result)
      rn <- c(0)
      limit <- round(0.05*(ncol(result) - 1)) # at lest present in 5% samples
      for(j in 1:nr){
        l <- length(which((result[j,] != 0)))
        if(l <= limit){
          rn <- c(rn, j)
        }
      }
      rn <- rn[-1]
      result <- result[-rn,]
      col_n <- ncol(result)
      for(ii in 2:col_n){
        result[,ii] <- result[,ii]/sum(result[,ii])
      }
      write.csv(result, "amp0.05.csv", row.names  = F)

      # caculates correlation
      amp <- read.csv("amp0.05.csv", header = T, sep = ',', row.names = 1)
      spe <- read.csv("merged_abundance_table_genus_cut0.05.tsv", header = T, sep = '\t', row.names = 1)
      spe <- spe/100 # in file spe, each col sum = 100.
      library("WGCNA")
      library("multtest")
      amp <- t(amp)
      spe <- t(spe)
      corr <- corAndPvalue(amp, spe, alternative = c("two.sided"), method = "spearman")
      # p value adjust part
      mtadj <- mt.rawp2adjp(unlist(corr$p), proc = "BH")
      adpcor <- mtadj$adjp[order(mtadj$index), 2]
      occor.p <- matrix(adpcor, dim(amp)[2])
      pvalue <- as.data.frame(occor.p)
      # remove the positive correlation part
      cor <- as.data.frame(corr$cor)
      rownames(pvalue) <- row.names(cor)
      colnames(pvalue) <- colnames(cor)
      cor[cor > 0] <- 0
      cor[pvalue > 0.05] <- 0
      write.csv(pvalue, "Pvalues-spearman-genus_metasub.csv",row.names = T)
      write.csv(cor, "Correlation-spearman-genus_metasub.csv",row.names = T)
    ```
  - Selected c_AMPs at least present to half cohort (here were 7).
    ```python{.line-numbers}
      #!/usr/bin/python3

      from numpy import savetxt, where
      from pandas import read_csv

      atch1 = read_csv("Cohort1.csv", index_col = 0)
      atch2 = read_csv("Cohort2.csv", index_col = 0)
      atch3 = read_csv("Cohort3.csv", index_col = 0)
      atch4 = read_csv("Cohort4.csv", index_col = 0)
      atch5 = read_csv("Cohort5.csv", index_col = 0)
      atch6 = read_csv("Cohort6.csv", index_col = 0)
      atch7 = read_csv("Cohort7.csv", index_col = 0)
      atch8 = read_csv("Cohort8.csv", index_col = 0)
      atch9 = read_csv("Cohort9.csv", index_col = 0)
      atch10 = read_csv("Cohort10.csv", index_col = 0)
      atch11 = read_csv("Cohort11.csv", index_col = 0)
      atch12 = read_csv("Cohort12.csv", index_col = 0)
      atch13 = read_csv("Cohort13.csv", index_col = 0)
      atch14 = read_csv("Cohort14.csv", index_col = 0)
      atch15 = read_csv("Cohort15.csv", index_col = 0)

      l_name = [atch1, atch2, atch3, atch4, atch5, atch6, atch7, atch8, atch9, atch10, atch11,  atch12, atch13, atch14, atch15]

      def get_dic(at4csv):
          colname = list(at4csv.columns)
          rowname = list(at4csv.index)
          ind = where(at4csv < 0)
          row_index = ind[0].tolist()
          col_index = ind[1].tolist()
          for i in range(len(rowname)):
              rowname[i] = rowname[i].replace("-", "_")
          a_dic = {}
          for i_ind in range(len(col_index)):
              new_key = rowname[row_index[i_ind]] + "," + colname[col_index[i_ind]]
              if new_key in a_dic.keys():
                  pass
              else:
                  a_dic[new_key] = namestr(at4csv, globals())[0]
          return a_dic

      def merge_dict(x,y):
          for k,v in x.items():
              if k in y.keys():
                  y[k] += "," + v
              else:
                  y[k] = v
          return y

      def namestr(obj, namespace):
          return [name for name in namespace if namespace[name] is obj]

      a_new = {}
      for it in l_name:
          a_new = merge_dict(a_new, get_dic(it))

      pr_l = ["target,soucre,numbers"]
      for i_key in a_new.keys():
          num = a_new[i_key].count(",") + 1
          if num >=  int(len(l_name)/2):
              pr = i_key + "," + str(a_new[i_key])
              #pr = i_key + "," + str(num) # show number of corhorts
              pr_l.append(pr)

      savetxt("Cytoscape_file_AtLeast7nameG.csv", pr_l, fmt = "%s")
    ```
    - Output file "Cytoscape_file_AtLeast7nameG.csv" look like this:
       |target|soucre|CH01|CH02|CH03|CH04|CH05|CH06|CH07|CH08|CH09|CH10|CH11|CH12|CH13|CH14|CH15|
       |:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
       |c_AMP_258|Actinomyces|atch4|atch1|atch8|atch5|atch15|atch7|atch3|
       |c_AMP_258|Rothia|atch4|atch2|atch1|atch9|atch12|atch13|atch7|atch3|
       |c_AMP_259|Staphylococcaceae_unclassified|atch4|atch2|atch1|atch8|atch9|atch6|atch7|
       |c_AMP_259|Staphylococcus|atch4|atch2|atch1|atch8|atch9|atch6|atch15|atch13|atch7|
       |c_AMP_259|Clostridiaceae_unclassified|atch4|atch2|atch1|atch9|atch6|atch12|atch7|

- Selected sequences were synthesis by chemical synthesis, then apply to _in vitro_ activity tests.
---
