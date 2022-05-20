#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH


if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_avlqc.sh /path/to/nda_root/ VM
Provide /path/to/nda_root/ and VM
VM name examples:
    dpstage for dpstage.dipr.partners.org
    rc-predict for rc-predict.bwh.harvard.edu
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
--eval "studies=[\"avlqc\"]" /data/predict/utility/avlqc_remove_study.js
echo ''

mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "db.metadata.remove({\"study\":\"avlqc\"})"
echo ''


# import new data
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate base && conda activate dpimport
# cd /data/predict/kcho/flow_test/
cd ${NDA_ROOT}
import.py -c /data/predict/dpimport/examples/$CONFIG "*/PHOENIX/GENERAL/*/processed/*/interviews/open/avlqc-*.csv"


# generate and import metadata
meta=avlqc_metadata.csv
echo 'Subject ID','Active','Consent','Study' > $meta
for i in `ls -d */PHOENIX/GENERAL/*/*/*/`
do
    echo `basename $i`,1,-,avlqc >> $meta
done
chgrp BWH-PREDICT-G $meta
chmod g+w $meta

import.py -c /data/predict/dpimport/examples/$CONFIG $meta

