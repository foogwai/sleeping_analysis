#! /usr/local/bin/bash
# This is used to generate CSSR related information

patients="ba fe fr gi me pa pe te to za"
stages="W E L R"


for p in $patients; do
  pdir="./cssr_output/${p}"
  rm -Rf $pdir
  mkdir $pdir
  for s in $stages; do
    for ((c=0; c<=30; c++)) do # there are 18-31 channels in different participant.
      printf 'Processing %s channel %s \n' $p $s
      fname="./out/${p}_${s}_channel_${c}_2500"
      frevname="./out/${p}_${s}_channel_${c}_2500_rev"
      #fname="./out/${p}_${s}_channel_${c}.txt"
      if [ -f "$fname" ]; then # ignore when source file not exists
        for ((l=2; l<=9; l++)) do # memory length (lambda) from 2 to 9
          lambda_fname="./cssr_output/${p}/${p}_${s}_channel_${c}_2500_${l}"
          lambda_frevname="./cssr_output/${p}/${p}_${s}_channel_${c}_2500_rev_${l}"
          #lambda_fname="./out/${p}_${s}_channel_${c}_${l}.txt"
          cp -fr $fname $lambda_fname
          cp -fr $frevname $lambda_frevname
          CSSR alpha.txt $lambda_fname $l -m
          CSSR alpha.txt $lambda_frevname $l -m
          rm -f $lambda_fname
          rm -f $lambda_frevname
          #CSSR alpha.txt $lambda_fname $l
        done
      fi
    done
  done
done