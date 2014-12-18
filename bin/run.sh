#!/bin/bash

# set -e

. bin/clean.sh
. bin/build.sh

files=`find -name '*.vrp' -not -path './input/*-tcc/*' | sort`
executions="1 2 3 4 5 6 7 8 9 10"

for e in $executions
do
    for i in $files
    do
        basename=`echo $i | sed 's/.*\/\(.*\).vrp/\1/'`
        vehicles=`echo $i | sed 's/.*-[a-zA-Z]*\([0-9]*\).*.vrp/\1/'`

        filename="out/$basename-$e.out"

        if [ ! -f $filename ]; then
            echo "Processing-$e $basename $vehicles"
            python run.py $i $vehicles > $filename || true
        else
            echo "$basename-$e already processed"
        fi
    done
done
