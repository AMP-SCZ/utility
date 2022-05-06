#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

# remove old data
mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "studies=[\"formqc\"]" /data/predict/utility/avlqc_remove_study.js
echo ''

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "db.metadata.remove({\"study\":\"formqc\"})"
echo ''


# import new data
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate && conda activate dpimport
cd /data/predict/kcho/flow_test/formqc/
import.py -c /data/predict/dpimport/examples/$CONFIG "formqc-*.csv"

exit

# generate and import metadata
meta=formqc_metadata.csv
echo 'Subject ID','Active','Consent','Study' > $meta
for i in `ls -d */*/*/`
do
    echo `basename $i`,1,-,formqc >> $meta
done
chgrp BWH-PREDICT-G $meta
chmod g+w $meta

import.py -c /data/predict/dpimport/examples/$CONFIG $meta

