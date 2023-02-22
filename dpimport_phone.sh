#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_phone.sh /path/to/nda_root/ VM
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
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=\"phone_\"" /data/predict/utility/remove_assess.js

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=\"actigraphy_\"" /data/predict/utility/remove_assess.js

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "assess=[\"dpgvail\",\"dppay\"]" /data/predict/utility/remove_assess.js

echo ''


# import new data
export PATH=/data/predict1/miniconda3/bin:$PATH
cd ${NDA_ROOT}
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/??-*.csv"
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/actigraphy/*/??-*.csv"


import.py -c $CONFIG "digitalqc/??-*.csv"
import.py -c $CONFIG "digitalqc/combined-*.csv"

