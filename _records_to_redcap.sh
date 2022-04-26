#!/bin/bash

# this wrapper script is essential because #BSUB -J redcap-import[1-$N]
# is not allowed within records_to_redcap.lsf

# clear previous logs
rm /data/predict/utility/bsub/*

export redcap_phoenix=/data/predict/kcho/flow_test/Pronet/PHOENIX/PROTECTED
export redcap_records=/data/predict/utility/bsub/redcap_records.txt
# export is to allow them to be used within records_to_redcap.lsf

cd $redcap_phoenix
find . -name *Pronet.json > $redcap_records
N=`cat $redcap_records | wc -l`

source /etc/profile
bsub -J "redcap-import[1-$N]%12" < /data/predict/utility/records_to_redcap.lsf

