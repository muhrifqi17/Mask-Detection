#!/bin/sh
rm mask.txt
rm no_mask.txt
for VARIABLE in $(ls results )
do
	for TES in $(ls results/$VARIABLE)
	do
		if [[ $TES =~ -No_Mask-true.txt$ ]]
		then
			echo $TES >> no_mask.txt
			cat results/$VARIABLE/$TES >> no_mask.txt

		elif [[ $TES =~ -Mask-true.txt$ ]]
		then
			echo $TES >> mask.txt
			cat results/$VARIABLE/$TES >> mask.txt
		fi
	done
done


