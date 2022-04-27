#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "studies=[\"avlqc\"]" /data/predict/utility/avlqc_remove_study.js
echo ''

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "db.metadata.remove({\"study\":\"avlqc\"})"
echo ''


# import new data
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate && conda activate dpimport
cd /data/predict/kcho/flow_test/Pronet/PHOENIX/GENERAL
import.py -c /data/predict/dpimport/examples/$CONFIG "*/processed/*/interviews/open/avlqc-*.csv"


# generate and import metadata
meta=avlqc_metadata.csv
echo 'Subject ID','Active','Consent','Study' > $meta
for i in `ls -d */*/*/`
do
    echo `basename $i`,1,-,avlqc >> $meta
done
chgrp BWH-PREDICT-G $meta
chmod g+w $meta

import.py -c /data/predict/dpimport/examples/$CONFIG $meta

