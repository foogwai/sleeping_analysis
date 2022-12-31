#! /usr/local/bin/bash
# This grabs the initial probability vector (in a column file) and the transition matrix (for each emitted symbol in a new file) from the CSSR output files 
# This is for each forward-time epsilon machine.

num_symbols=2 #aka |A| alphabet size, 2 for binary string
f2=" %1s"
patients="ba fe fr gi me pa pe te to za"
stages="W E"
skipped_log_file="forward_trans_skipped.txt"

rm -f $skipped_log_file
# Begin loop over each of participants, channels and stages
for p in $patients #loop over 10 patient.
do
	for a in $stages #loop over NREMe and wakeful
	do
		for lam in {2..10} #loop over 8 history lengths	
		do
			for ch in {0..30} #loop over 31 channels
			do
				filename="./cssr_output/${p}/${p}_${a}_channel_${ch}_2500_${lam}" # the name of the participant cssr files
				sourcename="./out/${p}_${a}_channel_${ch}_2500"
				if [ -f "$sourcename" ]; then
					echo 'Running for '"$filename"' ok here we go'
					###

					#Check that the _results file exists.
					# if exist do loop and get the initial probability and transition matrix
					# else skip
					if [ -f "$filename"_results ] #if the file exists
					then
						# Initial probabilities, taken from _results file
						rm -f "$filename"_inipi
						rm -f "$filename"_trans*
						grep 'P(state):' "$filename"_results | cut -d " " -f 2 >> "$filename"_inipi #make a new file with state distribution

						# Number of causal states N
						numstates=$(tail -n 1 "$filename"_info | grep -Eo '[0-9]+$') #This grabs the last line of _info, which reads 'Number of Inferred States: xxx' and grabs the number with grep

						#Create an array (N by N by |A|) of 0s, where N is number of states and |A| is number of symbols in alphabet
						declare -A trans # Or include it into trans[$i,$j,$k] like this
						for ((i=0;i<numstates;i++)) do #iterate from 0 to <numstates so it is N by N, but indexing starts at [0,0] because I have state 0 to state N-1
								for ((j=0;j<numstates;j++)) do
									for ((k=0;k<num_symbols;k++)) do
											trans[$i,$j,$k]=0
										done
								done
						done

						#here readingd 4 variables from either _inf.dot or _results file
						#but do this for every possible transition (N * 2)

						# Create a temp file with only useful information from _inf.dot
						tail -n +7 "$filename"_inf.dot > "$filename"_temp #create a temp file that only contains lines 7+ of _inf.dot file

						# Read the important parts (transition probabilities) from that temp file
						while IFS= read -r line; do
							from=$(echo $line |cut -d " " -f 1) #read from, the state that is transitioning from
							to=$(echo $line |cut -d " " -f 3) #read to, the state that is being transitioning to
							symbol=$(echo $line | cut -d " " -f 6 | cut -c 2) #read symbol, the emitted symbol on transition
							prob=$(echo $line |cut -d " " -f 7) #read value for the actual transition probabilty
							trans[$from,$to,$symbol]="$prob"
						#everything else can remain 0
						done < "$filename"_temp

						rm "$filename"_temp #remove _temp file

						# Now print each transition matrix to a file for each symbol
						for ((k=0;k<num_symbols;k++)) do
							for ((i=0;i<numstates;i++)) do
									for ((j=0;j<numstates;j++)) do
											printf "$f2" ${trans[$i,$j,$k]} >> "$filename"_trans"$k" #two separate files should have NxN matrices - one for each symbol type \\

								done
									echo >> "$filename"_trans"$k" #goes to a new line after printing each column value in a row

							done
						done

						unset trans # unset the matrix. This is maybe overkill but should be safe
						echo "$filename"' was a success.'
						echo 
					else #when the file does not exist
						echo "$filename"_results" did not exist. Skipping to the next file"
						echo "$filename" >> $skipped_log_file
						echo
					fi 	#end if statement over file existing
				fi	
			done
		done
	done
done

echo 'ALL DONE'