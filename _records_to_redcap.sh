#!/bin/bash

# this wrapper script is essential because #BSUB -J redcap-import[1-$N]
# is not allowed within records_to_redcap.lsf

redcap_records=/data/predict/utility/bsub/redcap_records.txt
redcap_phoenix=$1
redcap_dict=$2
API_TOKEN=$3
FORCE=1
export redcap_records redcap_phoenix redcap_dict API_TOKEN FORCE
# export is to allow them to be used within records_to_redcap.lsf

cd $redcap_phoenix
find . -name *Pronet.json > $redcap_records
N=`cat $redcap_records | wc -l`

source /etc/profile
# prevent getting thousand emails
export LSB_JOB_REPORT_MAIL=N
bsub -J "redcap-import[1-$N]%12" < /data/predict/utility/records_to_redcap.lsf

