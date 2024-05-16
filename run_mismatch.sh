#!/bin/bash

print_1="Merging Inputs and splitting"
print_2="Comparing Sync to Parents"
print_3="Running Sync Comparison Analysis"
print_4="Aggregating Results"
print_5="Cleaning Up"
print_6="-----------------------------"

names="4 3 7 5 8"
for chrom in $names
do
	echo $print_1

	gunzip ${chrom}.${1}.sync.gz #unzip input
	gunzip ${chrom}.${2}.sync.gz #unzip parental 1 sync
	gunzip ${chrom}.${3}.sync.gz #unzip parental 2 sync

	#combine syncs on position for splitting
	python split_for_mismatch.py --s ${chrom}.${1}.sync --p1 ${chrom}.${2}.sync --p2 ${chrom}.${3}.sync --rs 1 --rp 8

	gzip ${chrom}.${1}.sync #Zip syncs back up
	gzip ${chrom}.${2}.sync
	gzip ${chrom}.${3}.sync

	split mergedsyncs.csv ${chrom}. -l 10000 -da 6 --additional-suffix=.missplit.csv;

	python get_xargs_list_mismatch.py $chrom "1"; #make arguments for multirunning

	echo $print_2

	#run get_majorminor.py
	cat command_list_mismatch.txt | xargs -I CMD --max-procs=10 bash -c CMD; #run multiple python scripts

	echo $print_3

	python get_xargs_list_mismatch.py $chrom "2"; #make arguments for multirunning

	#run compare_sync_to_parents.py
	cat command_list_mismatch_2.txt | xargs -I CMD --max-procs=10 bash -c CMD; #run multiple python scripts

	echo $print_4

	python get_xargs_list_mismatch.py $chrom "3"; #make arguments for multirunning

	#run add_subset_files_mismatch.py
	echo "ind,chr,mismatch,mismatch_sub,p1M,p2M,p1m,p2m,cm,cmp1,cmp2,cmf2,total" >> ${chrom}_aggregate.csv
	cat command_list_mismatch_3.txt | xargs -I CMD --max-procs=10 bash -c CMD; #run multiple python scripts

	python final_tally.py --f ${chrom}_aggregate.csv --o $1 --p1 $2 --p2 $3

	echo $print_5

	#remove intermediates
	rm mergedsyncs.csv
	rm *.missplit.csv
	rm command_list_mismatch.txt
	rm *_majorminors.csv
	rm command_list_mismatch_2.txt
	rm *_mismatchtally.csv
	rm command_list_mismatch_3.txt
	rm *_aggregate.csv
	echo $print_6
done
