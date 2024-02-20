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

# clean duplicate arms
clean_old_arm.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ $TOKEN

# set umask and group to avoid permission issue for team members
umask 007 && newgrp BWH-PREDICT-G

# download REDCap JSONs
down_mgb_redcap_records.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ $TOKEN

# shift their dates
shift_redcap_dates.py /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/ "*/raw/*/surveys/*.Prescient.json" /data/predict1/utility/rpms-to-yale/CloneOfYaleRealRecords_DataDictionary_2023-03-21_calc_to_text_checkbox.csv

