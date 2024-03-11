#!/bin/bash

if [ "$1" == "-h" ]
then
    echo Usage: $0 /path/to/wisc_v01_*csv
    exit
elif [ $# -lt 1 ]
then
    file=/data/predict1/to_nda/nda-submissions/network_combined/wisc_v01_baseline.csv
else
    file=$1
fi

newfile=${file/wisc_v/wais_iv_part1}

sed "s/wisc_v/wais_iv_part1/g" $file > $newfile

