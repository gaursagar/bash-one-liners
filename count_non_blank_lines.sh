#!/bin/bash

for i in `ls *xyz`;do 
	echo $i; 
	cat $i | sed -n '3,$p' | sed '/^\s*$/d' | wc -l;
	# cat | trim a range if needed | remove blanks | wc
done
