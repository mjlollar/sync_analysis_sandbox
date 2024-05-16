#!/bin/bash

names="<your_names>"

for name in $names
do
	echo $name
	./run_mismatch.sh $name <parent1> <parent2>
done
