#!/bin/bash

print_1="spliting syncs, chrom:"
print_2="running sync analysis"
print_3="removing intermediates"
print_4="Combining and adding to results"
print_5="------------------"

names="4 3 7 5 8"
for chrom in $names
do
	echo $print_1
	echo $chrom
	split ${chrom}.${1}.sync ${chrom}. -l 10000 -da 4 --additional-suffix=.split.sync;
	python get_xargs_list.py $chrom;
	echo $print_2
	cat command_list.txt | xargs -I CMD --max-procs=6 bash -c CMD;
	echo $print_3
	rm *.split.sync;
	rm command_list.txt;
	echo $print_4
	python add_subset_files.py --f ${chrom}_singlesync_results.csv --i ${1} --c ${chrom}
	echo $print_5
done
