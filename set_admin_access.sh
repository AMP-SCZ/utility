#!/bin/bash

MONGO_UID=${1:-dpdash}

export PATH=/data/predict1/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $HOST ] || [ -z $PORT ] || [ -z $state ] || [ -z $MONGO_PASS ] || [ -z $CONFIG ]
then
    echo Define HOST, PORT, state, MONGO_PASS, CONFIG and try again
    exit 1
fi


mongo --tls --tlsCAFile $state/ssl/ca/cacert.pem \
--tlsCertificateKeyFile $state/ssl/mongo_client.pem \
mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin \
--eval "uid=\"$MONGO_UID\"" \
/data/predict/utility/_set_admin_access.js


