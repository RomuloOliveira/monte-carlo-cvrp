#!/bin/bash

set -e

. bin/clean.sh
. bin/build.sh

files=`find -name '*.vrp' -not -path './input/*-tcc/*' | sort`
for i in $files
do
    basename=`echo $i | sed 's/.*\/\(.*\).vrp/\1/'`
    vehicles=`echo $i | sed 's/.*-[a-zA-Z]*\([0-9]*\).*.vrp/\1/'`

    executions="1 2 3 4 5"
    for e in $executions
    do
        filename="out/$basename-$e.out"
        echo "Processing-$e $basename $vehicles"
        python run.py $i $vehicles > $filename
    done
done
