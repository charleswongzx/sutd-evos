#!/bin/bash

echo Updating datatypes

for lcm_file in ./*.lcm; do
	lcm-gen -p "$lcm_file"
	echo Updating "$lcm_file".
done

for py_file in ./exlcm/*.py; do
	echo Copying "$py_file".
	cp "$py_file" ../exlcm
done

echo Update complete.
