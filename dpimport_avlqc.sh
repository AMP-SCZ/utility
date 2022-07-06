#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH


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


source /data/predict/utility/.vault/.env.${2}

# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=[\"interviewMonoAudioQC_open\",\"interviewVideoQC_open\",\"interviewRedactedTranscriptQC_open\",\"interviewMonoAudioQC_psychs\",\"interviewMonoVideoQC_psychs\",\"interviewRedactedTranscriptQC_psychs\"]" /data/predict/utility/remove_assess.js
echo ''


# import new data
export PATH=/data/predict/miniconda3/bin/:$PATH
cd ${NDA_ROOT}
# temporary renaming, will be removed after
# https://github.com/dptools/process_offsite_audio/pull/1 is merged
/data/predict/utility/avlqc_to_site.py $NDA_ROOT
import.py -c /data/predict/dpimport/examples/$CONFIG "*/PHOENIX/GENERAL/*/processed/*/interviews/*/??-*-interview*day*.csv"


