#!/bin/bash

# this wrapper script is essential because #BSUB -J redcap-import[1-$N]
# is not allowed within records_to_redcap.lsf

if [ $# -lt 3 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo """Usage:
./_rpms_to_redcap.sh /path/to/PHOENIX/PROTECTED/ /redcap/dict/dir/ API_TOKEN"""
    exit 1
fi

redcap_records=/data/predict1/utility/bsub/rpms_records.txt
redcap_phoenix=$1
redcap_dict=$2
API_TOKEN=$3
FORCE=0
export redcap_records redcap_phoenix redcap_dict API_TOKEN FORCE
# export is to allow them to be used within records_to_redcap.lsf

# echo 'Deleting old records ...'
export PATH=/data/predict1/miniconda3/bin/:$PATH
# /data/predict1/utility/delete_redcap_records.py $redcap_phoenix $API_TOKEN

echo  'Uploading new records ...'
cd $redcap_phoenix
if [ -f rpms_records.txt ]
then
    # rpms_records.txt should consist of selective records
    # instead of all records under $redcap_phoenix
    redcap_records=${redcap_phoenix}/rpms_records.txt
else
    ls -d Prescient??/raw/*/surveys > $redcap_records
fi

N=`cat $redcap_records | wc -l`

source /etc/profile
# prevent getting thousand emails
export LSB_JOB_REPORT_MAIL=N
bsub -J "redcap-import[1-$N]%12" < /data/predict1/utility/rpms_to_redcap.lsf

