#!/usr/bin/env bash

# do not change the base name:
# combined-AMPSCZ-day1to1.csv
# base hash:
# 813e15eb4006956b1d804e211ce95c656bc1704e625c718630d21343a85bc617

export PATH=/data/predict1/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_mriqc.sh /path/to/nda_root/ VM
Provide /path/to/nda_root/ and VM
VM name examples:
    dpstage for dpstage.dipr.partners.org
    rc-predict for rc-predict.bwh.harvard.edu
    rc-predict-dev for rc-predict-dev.bwh.harvard.edu
    It is the first part of the server name."""
    exit
else
    export NDA_ROOT=$1
fi

source /data/predict1/utility/.vault/.env.${2}

: << COMMENT
# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin --eval "assess=[\"mriqc\",\"eegcount\",\"mricount\",\"mriqcval\", \"mridataflow\"]" /data/predict1/utility/remove_assess.js
COMMENT

# import new data
export PATH=/data/predict1/miniconda3/bin:$PATH
cd ${NDA_ROOT}

# mridataflow checker
import.py -c $CONFIG "MRI_ROOT/flow_check/*mridataflow-day1to*.csv"

# project level data
import.py -c $CONFIG "MRI_ROOT/derivatives/quick_qc/combined-*-mriqc-day1to*.csv"

# subject level data
import.py -c $CONFIG "MRI_ROOT/derivatives/quick_qc/*/??-*-mriqc-day1to*.csv"

# eeg count, mri count, mri qc final score
import.py -c $CONFIG "MRI_ROOT/eeg_mri_count/??-*-day1to*.csv"

