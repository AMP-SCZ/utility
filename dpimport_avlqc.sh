#!/usr/bin/env bash

export PATH=/data/predict1/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH


if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_avlqc.sh /path/to/nda_root/ VM
Provide /path/to/nda_root/ and VM
VM name examples:
    dpstage for dpstage.dipr.partners.org
    rc-predict for rc-predict.bwh.harvard.edu
    It is the first part of the server name."""
    exit
else
    export NDA_ROOT=$1
fi


source /data/predict1/utility/.vault/.env.${2}

: << COMMENT
# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=[\"interviewMonoAudioQC_open\",\"interviewVideoQC_open\",\"interviewRedactedTranscriptQC_open\",\"interviewMonoAudioQC_psychs\",\"interviewVideoQC_psychs\",\"interviewRedactedTranscriptQC_psychs\",\"avlqc\",\"open_count\",\"psychs_count\",\"subject_count\"]" /data/predict1/utility/remove_assess.js
echo ''
COMMENT

# import new data
export PATH=/data/predict1/miniconda3/bin/:$PATH
cd ${NDA_ROOT}
import.py -c $CONFIG "*/PHOENIX/GENERAL/*/processed/*/interviews/*/??-*-interview*day*.csv"


cd AVL_quick_qc
rm -rf *

/data/predict1/utility/combine_avlqc.py ${NDA_ROOT}
assess=avlqc
name=combined
cat ${name}-PRONET-${assess}-day1to1.csv > ${name}-AMPSCZ-avlqc-day1to1.csv
tail -n +2 ${name}-PRESCIENT-${assess}-day1to1.csv >> ${name}-AMPSCZ-${assess}-day1to1.csv
/data/predict1/utility/renumber_days.py ${name}-AMPSCZ-${assess}-day1to1.csv

import.py -c $CONFIG "combined-*-avlqc-day1to1.csv"
import.py -c $CONFIG "*_count/??-*-*_count-day1to*csv"

