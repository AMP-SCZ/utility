#!/bin/bash

export PATH=/data/predict/miniconda3/bin:$PATH

if [ $# -lt 3 ] || [ $1 = '-h' ] || [ $1 == '--help' ]
then
    echo """./submit.sh ndar_subject01 tashrif 1234
Provide NDA dict name, submitter's NDA user name, and NDA collection ID"""
    exit
fi

form=$1
user=$2
collection=$3
root=/data/predict1
datestamp=$(date +"%Y%m%d")

for network in Pronet Prescient
do
    prefix=${form}_${network}
    title=${prefix}_${datestamp}
    data=${prefix}.csv
    python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
    -u $user -c $collection -b -t $title \
    $root/to_nda/nda-submissions/$data
done


