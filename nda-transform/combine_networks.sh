#!/bin/bash

export PATH=/data/predict1/miniconda3/bin:$PATH

_help()
{
    echo """Usage:
./submit.sh -u tashrif -f ndar_subject01 -n Pronet -e baseline
./submit.sh -u tashrif -f ndar_subject01 -n Prescient
./submit.sh -u tashrif -f ndar_subject01
./submit.sh -f ndar_subject01

Mandatory:
-f : NDA dict name 

Optional:
-u : submitter's NDA username
-n : network
-e : event

nda-submission directory is globed for \${f}_\${n}_\${e}.csv to find files to submit
do not provide -u for only validation
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

if [ -z $form ]
then
    _help
fi


collection=PROD-AMPSCZ
root=/data/predict1
datestamp=$(date +"%Y%m%d")

# determine output name
if [ -z $event ]
then
    data=$root/to_nda/nda-submissions/network_combined/${form}.csv
else
    data=$root/to_nda/nda-submissions/network_combined/${form}_${event}.csv
fi


files=`ls $root/to_nda/nda-submissions/${form}*${network}*${event}.csv`
# populate header
for file in $files
do
    head -n 2 $file > $data
    break 1
done


# append form CSVs
for file in $files
do
    tail -n +3 $file >> $data
done

echo Processing $data

if [ -z $user ]
then
    # validate only
    python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
    $data

else
   echo Use utility/nda-transform/submit.sh 
fi

echo ''

