#!/usr/bin/env bash

export PATH=/data/predict1/mongodb-linux-x86_64-rhel70-4.4.20/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """$0 /path/to/nda_root/ VM
Provide /path/to/nda_root/ and VM
VM name examples:
    dpstage for dpstage.dipr.partners.org
    rc-predict for rc-predict.bwh.harvard.edu
    rc-predict-dev for rc-predict-dev.bwh.harvard.edu
    It is the first part of the server name.

This script does incremental import by default.
Provide 1 at the end to erase existing data and do a fresh import:
    $0 /path/to/nda_root VM 1"""
    exit
else
    export NDA_ROOT=$1
fi

source /data/predict1/utility/.vault/.env.${2}

if [ "$3" == 1 ]
then
# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=\"form_\"" /data/predict1/utility/remove_assess.js
echo ''
fi

# import new data
export PATH=/data/predict1/miniconda3/bin/:$PATH
cd ${NDA_ROOT}/formqc

# subject level data
import.py -c $CONFIG "??-*-form_*-day1to*.csv" -n 8

# project level data
# do it in multiple steps to circumvent unknown mongo timeout
import.py -c $CONFIG "combined-??-form_*-day1to*.csv" -n 4
# import.py -c $CONFIG "combined-PRONET-form_*-day1to*.csv"
# import.py -c $CONFIG "combined-PRESCIENT-form_*-day1to*.csv"
# import.py -c $CONFIG "combined-AMPSCZ-form_*-day1to*.csv"
import.py -c $CONFIG "combined-PR*-form_screening-day1to*.csv" -n 2
import.py -c $CONFIG "combined-PR*-form_baseline-day1to*.csv" -n 2
import.py -c $CONFIG "combined-PR*-form_conversion-day1to*.csv" -n 2
import.py -c $CONFIG "combined-PR*-form_floating-day1to*.csv" -n 2

