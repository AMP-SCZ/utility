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
down_mgb_redcap_records.py $PHOENIX_PROTECTED $TOKEN

# shift their dates
shift_redcap_dates.py $PHOENIX_PROTECTED "*/raw/*/surveys/*.Prescient.json" /data/predict1/utility/yale-real/*_DataDictionary_*.csv

# explicit permission change
n=Prescient
GENERAL=${PHOENIX_PROTECTED/PROTECTED/GENERAL}
for E in ${GENERAL}/${n}??/processed/ \
    ${GENERAL}/${n}??/processed/* \
    ${GENERAL}/${n}??/processed/*/surveys/ \
    ${GENERAL}/${n}??/processed/*/surveys/???????.${n}.json
do
    chgrp BWH-PREDICT-G $E
    chmod g+w $E
done
