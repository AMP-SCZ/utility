#!/usr/bin/env bash

# do not change the base name:
# combined-AMPSCZ-day1to1.csv
# base hash:
# 813e15eb4006956b1d804e211ce95c656bc1704e625c718630d21343a85bc617

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_eegqc.sh /path/to/nda_root/ VM
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

source /data/predict/utility/.vault/.env.${2}

# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin --eval "assess=[\"mriqc\"]" /data/predict/utility/remove_assess.js

# import new data
export PATH=/data/predict/miniconda3/bin:$PATH
cd ${NDA_ROOT}

# project level data
import.py -c /data/predict/dpimport/examples/$CONFIG MRI_ROOT/derivatives/quick_qc/combined-*-mriqc-day1to*.csv

# subject level data
import.py -c /data/predict/dpimport/examples/$CONFIG "MRI_ROOT/derivatives/quick_qc/*/??-???????-mriqc-day1to*.csv"

