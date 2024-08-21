#!/bin/bash

if [ "$1" == "-h" ] || [ $# == 0 ]
then
    echo """Usage:
$0 1234567890
Provide REDCap API token
"""
    exit
fi


TOKEN=$1

export PATH=/data/predict1/miniconda3/bin/:/data/predict1/utility/:$PATH
PHOENIX_PROTECTED=/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED

# clean duplicate arms
clean_old_arm.py $PHOENIX_PROTECTED $TOKEN

# download REDCap JSONs
down_mgb_redcap_records.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ $TOKEN
chgrp BWH-PREDICT-G ${PHOENIX_PROTECTED}/Prescient??/raw/*/surveys/???????.Prescient.json

# shift their dates
shift_redcap_dates.py $PHOENIX_PROTECTED "*/raw/*/surveys/*.Prescient.json" /data/predict1/utility/yale-real/CloneOfYaleRealRecords_DataDictionary_2024-04-16.csv
chgrp BWH-PREDICT-G ${PHOENIX_PROTECTED/PROTECTED/GENERAL}/Prescient??/processed/*/surveys/???????.Prescient.json

