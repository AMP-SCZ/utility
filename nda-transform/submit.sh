#!/bin/bash

export PATH=/data/predict/miniconda3/bin:$PATH

if [ $# -lt 2 ] || [ $1 = '-h' ] || [ $1 == '--help' ]
then
    echo """Usage:
./submit.sh ndar_subject01 tashrif
./submit.sh ndar_subject01 tashrif Prescient
Provide NDA dict name & submitter's NDA username
Network name is optional. It is useful when you will have to retry just one submission."""
    exit
fi

form=$1
user=$2
collection=PROD-AMPSCZ
root=/data/predict1
datestamp=$(date +"%Y%m%d")

if [ ! -z $3 ]
then
    network=$3
else
    network="Pronet Prescient"
fi

for net in $network
do
    prefix=${form}_${net}
    title=${prefix}_${datestamp}
    data=${prefix}.csv
    python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
    -u $user -t $title -d $title \
    -a $collection \
    -b $root/to_nda/nda-submissions/$data
    
    # the wait maybe useful
    sleep 30
done


