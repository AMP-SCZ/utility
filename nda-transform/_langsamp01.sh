#!/bin/bash

export PATH=/data/predict1/miniconda3/bin/:$PATH

_help()
{
    echo """Usage:
$0 TYPE
Accepted types are OPEN or PSYCHS only
"""
    exit
}


if [ $# == 0 ] || [ "$1" == "-h" ]
then
    _help
fi


if [ "$1" == OPEN ]
then
    prefix=chrspeech
elif [ "$1" == PSYCHS ]
then
    prefix=chrpsychs_av
else
    _help
fi


for n in Pronet Prescient
do
    echo $n
    for e in screening baseline month_1 month_2
    do
        echo $e
        ./generate.sh -f langsamp01 -n $n -e $e -p $prefix \
        -o "--data /data/predict1/to_nda/nda-submissions/langsamp01/${n}_${1}_inventory_no_prescreen.csv"
        echo
    done
done


s=`echo "$1" | tr '[:upper:]' '[:lower:]'`
for e in screening baseline month_1 month_2
do
    echo $e
    ./combine_networks.sh -e $e -s $s -f langsamp01
    echo
done


