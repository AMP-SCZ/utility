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

# kill any prior stuck imports
# pkill --signal 9 import.py

# import new data
export PATH=/data/predict1/miniconda3/bin/:$PATH

cd ${NDA_ROOT}
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_informed_consent_run_sheet-day1to*.csv" -n 1
sleep 120
echo
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_inclusionexclusion_criteria_review-day1to*.csv" -n 1
sleep 120
echo
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_sociodemographics-day1to*.csv" -n 1
sleep 120
echo
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_dpdash_charts-day1to*.csv" -n 1


