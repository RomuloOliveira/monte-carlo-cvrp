#!/bin/bash

. bin/clean.sh
. bin/build.sh

files=`find -name '*.vrp' | sort`
for i in $files
do
    basename=`echo $i | sed 's/.*\/\(.*\).vrp/\1/'`
    vehicles=`echo $i | sed 's/.*-[a-zA-Z]*\([0-9]*\).*.vrp/\1/'`
    filename="out/$basename.out"

    echo "Processing $basename $vehicles"
    python run.py $i $vehicles > $filename
done
