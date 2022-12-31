#!/usr/local/bin/bash
# for reversed time
# This file converts all ';' delimiters in the *_state_series to ',' instead just for Matlab.
#
# # # Output
# *_comma files (forward time here_
patients="ba fe fr gi me pa pe te to za"
stages="W E"


for p in $patients #loop over 10 paticipants.
do
	for a in $stages #loop over WR NREMe
	do
		for lam in {2..9} #loop over 8 history lengths	
		do
			for ch in {0..30} #loop over 31 channels
			do
				filename="../cssr_output/${p}/${p}_${a}_channel_${ch}_2500_rev_${lam}" # "$filename"
				echo 'attempting delimiter for '"$filename"' ok here we go'
				###

				#Check that the *_state_series file exists so can fix delimiter. If it does not exist we skip to the next file.
				# else skip
				if [ -f "$filename"_state_series ] #if the _state_series file exists
				then
					sed -i -e 's/;/,/g' "$filename"_state_series

					echo "$filename"' forward time comma delimit was a success.'
					echo 
				else
					echo "$filename"_state_series" did not exist. Skipping to the next file"
					echo "$filename" >> skippedcomma.txt # files in here didn't exist

					echo
				fi 	#end if statement over file existing
	
			done
		done
	done
done

echo 'ALL DONE'