#!/bin/bash

_help()
{
    echo """Usage:
$0 -e baseline
$0 -f /path/to/wisc_v01_*csv

if -e is provided, network_combined/wisc_v01_baseline.csv is used as -f
"""

    exit
}

while getopts "e:f:" i
do
    case $i in
        e) event=$OPTARG ;;
        f) file=$OPTARG ;;
        ?) _help ;;
    esac
done

if [ ! -z $event ]
then
    file=/data/predict1/to_nda/nda-submissions/network_combined/wisc_v01_${event}.csv
fi

newfile=${file/wisc_v/wais_iv_part1}

sed "s/wisc_v/wais_iv_part1/g" $file > $newfile

