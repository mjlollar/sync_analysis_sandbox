#!/bin/bash

names="TF56 PB-6"
for name in $names
do
	echo $name
	./run_syncs.sh $name
done
