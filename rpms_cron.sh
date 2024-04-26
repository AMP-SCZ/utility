#!/bin/bash

datestamp=$(date +"%d.%m.%Y")
mkdir -p /mnt/prescient/one_day_backup/
rm /mnt/prescient/one_day_backup/*
cp /mnt/prescient/RPMS_incoming/*_${datestamp}.csv /mnt/prescient/one_day_backup/

export PATH=$HOME/miniconda3/bin/:/mnt/prescient/utility/:$PATH

rename_RPMS_vars.py /mnt/prescient/RPMS_incoming/ && \
replace_RPMS_values.py /mnt/prescient/RPMS_incoming/ && \
rpms_psychs_partition.py /mnt/prescient/RPMS_incoming/

