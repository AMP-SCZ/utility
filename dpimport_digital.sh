#!/usr/bin/env bash

export PATH=/data/predict1/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

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
--eval "assess=\"phone_\"" /data/predict1/utility/remove_assess.js

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=\"actigraphy_\"" /data/predict1/utility/remove_assess.js

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=\"watch_\"" /data/predict1/utility/remove_assess.js

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=[\"dpgvail\",\"dppay\",\"dpaxty\"]" /data/predict1/utility/remove_assess.js

echo ''
fi

# import new data
export PATH=/data/predict1/miniconda3/bin:$PATH
cd ${NDA_ROOT}
# import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/??-*.csv"
# import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/actigraphy/*/??-*.csv"

# selective phone data import
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/??-*phone_month_view*.csv" -n 2
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/??-*phone_accel_availability24h_daily*.csv" -n 2
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/??-*actigraphy_month_view*.csv" -n 2
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/??-*dpgvail*.csv" -n 2

import.py -c $CONFIG "digitalqc/??-*.csv" -n 2
import.py -c $CONFIG "digitalqc/combined-*.csv"

