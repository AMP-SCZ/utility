#!/bin/bash

datestamp=$(date +"%d.%m.%Y")
INCOMING=/var/lib/prescient/RPMS_incoming
BACKUP=/var/lib/prescient/one_day_backup

mkdir -p $BACKUP
rm ${BACKUP}/*
cp ${INCOMING}/*_${datestamp}.csv ${BACKUP}/

export PATH=$HOME/miniconda3/bin/:/var/lib/prescient/utility/:$PATH

rename_RPMS_vars.py $INCOMING && \
replace_RPMS_values.py $INCOMING && \
rpms_psychs_partition.py $INCOMING

