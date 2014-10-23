#!/bin/bash

. bin/clean.sh
. bin/build.sh

files=`find -name '*.vrp'`
for i in $files
do
    basename=`echo $i | sed 's/.*\/\(.*\).vrp/\1/'`
    vehicles=`echo $i | sed 's/.*-k\(.*\).vrp/\1/'`
    filename="out/$basename.out"

    echo "Processing $basename"
    python run.py $i $vehicles > $filename
done
