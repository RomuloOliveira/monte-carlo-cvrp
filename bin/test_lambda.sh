#!/bin/bash

# set -e

. bin/clean.sh
. bin/build.sh

instances="./input/Augerat/A-n32-k5.vrp ./input/Takes/A-n65-k9.vrp"

lambdas_p="0.0025 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0"
for lambda_p in $lambdas_p
do
    for instance in $instances
    do
        basename=`echo $instance | sed 's/.*\/\(.*\).vrp/\1/'`
        vehicles=`echo $instance | sed 's/.*-[a-zA-Z]*\([0-9]*\).*.vrp/\1/'`
        filename="out/$basename-$lambda_p.out"
        echo "Processing $basename with $vehicles vehicles and lambda_p=$lambda_p > $filename"
        python run.py $instance $vehicles > $filename
    done
done
