#!/bin/bash

datestamp=$(date +"%d.%m.%Y")
INCOMING=/var/lib/prescient/RPMS_incoming
BACKUP=/var/lib/prescient/one_day_backup
export PATH=$HOME/miniconda3/bin/:/var/lib/prescient/utility/:$PATH

# poll INCOMING folder for *_datestamp.csv files
# execute this workflow only when export is complete
while [ 1 ]
do
    count=`ls ${INCOMING}/*_${datestamp}.csv | wc -l`
    if [ $count -lt 76 ]
    then
        sleep 120
    else
        break
    fi
done

mkdir -p $BACKUP
rm ${BACKUP}/*
cp ${INCOMING}/*_${datestamp}.csv ${BACKUP}/

rename_RPMS_vars.py $INCOMING && \
replace_RPMS_values.py $INCOMING && \
rpms_psychs_partition.py $INCOMING

