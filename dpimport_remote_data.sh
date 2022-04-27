#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH


if [ -z $HOST ] || [ -z $PORT ] || [ -z $state ] || [ -z $MONGO_PASS ] || [ -z $CONFIG ]
then
    echo Define HOST, PORT, state, MONGO_PASS, CONFIG and try again
    exit 1
fi

echo Importing to mongodb://dpdash:MONGO_PASS@$HOST:$PORT
echo ''

# delete old collections
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin /data/predict/utility/remove_studies.js

# import new collections
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate && conda activate dpimport

cd /data/predict/kcho/flow_test/

# metadata
import.py -c /data/predict/dpimport/examples/$CONFIG files_metadata.csv
import.py -c /data/predict/dpimport/examples/$CONFIG "*_status/*_metadata.csv"

# project level files status
import.py -c /data/predict/dpimport/examples/$CONFIG "*_status/files-*-flowcheck-day1to9999.csv"

# subject level files status
import.py -c /data/predict/dpimport/examples/$CONFIG "*_status/*-flowcheck-day1to1.csv"

