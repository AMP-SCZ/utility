#!/bin/bash

# this wrapper script is essential because #BSUB -J redcap-import[1-$N]
# is not allowed within records_to_redcap.lsf

if [ $# -lt 3 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo """Usage:
./_records_to_redcap.sh /path/to/PHOENIX/PROTECTED/ /redcap/dict/dir/ API_TOKEN"""
    exit 1
fi

redcap_records=/data/predict/utility/bsub/redcap_records.txt
redcap_phoenix=$1
redcap_dict=$2
API_TOKEN=$3
FORCE=1
export redcap_records redcap_phoenix redcap_dict API_TOKEN FORCE
# export is to allow them to be used within records_to_redcap.lsf

echo 'Deleting old records ...'
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate base && \
conda activate dpimport && \
/data/predict/utility/delete_redcap_records.py $redcap_phoenix $API_TOKEN

echo  'Uploading new records ...'
cd $redcap_phoenix
find . -name *Pronet.json > $redcap_records
N=`cat $redcap_records | wc -l`

source /etc/profile
# prevent getting thousand emails
export LSB_JOB_REPORT_MAIL=N
bsub -J "redcap-import[1-$N]%12" < /data/predict/utility/records_to_redcap.lsf

