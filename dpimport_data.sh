#!/usr/bin/env bash

if [ -z $state ] || [ -z $MONGO_PASS ]
then
    echo Define state and MONGO_PASS and try again
    exit 1
fi

# delete old collections
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem --tlsCertificateKeyFile $state/ssl/mongo_client.pem mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdata?authSource=admin /data/predict/utility/remove_studies.js

# import new collections
source /opt/dpdash/miniconda3/bin/activate && \

cd /data/predict/kcho/flow_test/ && \

# metadata
import.py -c /opt/dpdash/dpimport/examples/config.yml files_metadata.csv && \
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/*_metadata.csv" && \

# project level files status
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/files-*-flowcheck-day1to9999.csv" && \

# subject level files status
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/*-flowcheck-day1to1.csv"

