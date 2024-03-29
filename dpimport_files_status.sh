#!/usr/bin/env bash

export PATH=/data/predict1/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_files_status.sh /path/to/nda_root/ VM
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

echo Importing to mongodb://dpdash:MONGO_PASS@$HOST:$PORT
echo ''

: << COMMENT
# delete old collections
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin --eval "assess=[\"flowcheck\",\"data_baseline\",\"data_month_2\"]" /data/predict1/utility/remove_assess.js

# delete metadata
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin /data/predict1/utility/remove_metadata.js
COMMENT

# import new collections
export PATH=/data/predict1/miniconda3/bin:$PATH
cd $NDA_ROOT

# metadata
import.py -c $CONFIG combined_metadata.csv
import.py -c $CONFIG "*_status/*_metadata.csv"

# project level files status
import.py -c $CONFIG "combined-AMPSCZ-data_*-day1to1.csv"
import.py -c $CONFIG "*_status/combined-*-data_*-day1to1.csv"

# subject level files status
import.py -c $CONFIG "*_status/??-*-data_*-day1to1.csv"

