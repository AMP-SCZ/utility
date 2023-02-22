#!/bin/bash

export PATH=/data/predict1/miniconda3/bin:$PATH

_help()
{
    echo """Usage:
./submit.sh -u tashrif -f ndar_subject01 -n Pronet -e baseline
./submit.sh -u tashrif -f ndar_subject01 -n Prescient
./submit.sh -u tashrif -f ndar_subject01

Mandatory:
-f : NDA dict name 
-u : submitter's NDA username

Optional:
-n : network
-e : event

nda-submission directory is globed for \${f}_\${n}_\${e}.csv to find files to submit
"""

    exit
}


while getopts "u:f:n:e:" i
do
    case $i in
        u) user=$OPTARG ;;
        f) form=$OPTARG ;;
        n) network=$OPTARG ;;
        e) event=$OPTARG ;;
        ?) _help ;;
    esac
done


collection=PROD-AMPSCZ
root=/data/predict1
datestamp=$(date +"%Y%m%d")


for data in `ls $root/to_nda/nda-submissions/${form}*${network}*${event}.csv`
do
    echo Processing $data

    title=`basename ${data/.csv/}`
    python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
    -u $user -t $title -d $title \
    -a $collection \
    -b $data
    
    echo ''
    # the wait maybe useful
    sleep 30
done


