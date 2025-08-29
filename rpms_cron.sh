#!/bin/bash

export HOSTNAME=1200941-Prescient.orygen.org.au

# provide a way to define datestamp from outside of this script
if [ -z $datestamp ]
then
    datestamp=$(date +"%d.%m.%Y")
fi

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
        echo
        echo Processing started at $(date +%H:%M)
        break
    fi
done

mkdir -p $BACKUP
# back up only if the files have not been backed up before
count=`ls ${BACKUP}/*_${datestamp}.csv | wc -l`
if [ $count -lt 76 ]
then
    rm ${BACKUP}/*
    cp ${INCOMING}/*_${datestamp}.csv ${BACKUP}/
fi

rename_RPMS_vars.py $INCOMING ${datestamp}.csv && \
replace_RPMS_values.py $INCOMING ${datestamp}.csv && \
rpms_psychs_partition.py $INCOMING ${datestamp}.csv && \
convert_cbc_units.py $INCOMING && \
rm $INCOMING/.complete_* && \
touch $INCOMING/.complete_${datestamp}

echo
echo Processing ended at $(date +%H:%M)


