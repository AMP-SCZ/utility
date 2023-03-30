#!/usr/bin/env bash

export PATH=/data/predict1/mongodb-database-tools-rhel70-x86_64-100.5.2/bin:$PATH

if [ -z $1 ]
then
    echo """./backup_mongodb.sh VM
VM name examples:
    dpstage for dpstage.dipr.partners.org
    rc-predict for rc-predict.bwh.harvard.edu
    rc-predict-dev for rc-predict-dev.bwh.harvard.edu
    It is the first part of the server name."""
    exit
fi

source /data/predict1/utility/.vault/.env.${1}

if [ -z $HOST ] || [ -z $PORT ] || [ -z $state ] || [ -z $MONGO_PASS ]
then
    echo Define HOST, PORT, state, MONGO_PASS and try again
    exit 1
fi


export GODEBUG=x509ignoreCN=0
datestamp=$(date +"%Y%m%d")

cd /data/predict1/predict-mongodb-backup/

# export from mongodb

# dpdmongo:users
mongoexport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdmongo?authSource=admin" --collection=users --out=users_${datestamp}.json


# dpdmongo:configs
mongoexport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdmongo?authSource=admin" --collection=configs --out=configs_${datestamp}.json


# dpdata:charts
mongoexport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin" --collection=charts --out=charts_${datestamp}.json



source /data/pnl/soft/pnlpipe3/duply_backup/.aws-keys
export PATH=/data/predict1/aws-cli/bin:$PATH

if [ -z $AWS_ACCESS_KEY_ID ] || [ -z $AWS_SECRET_ACCESS_KEY ]
then
    echo Define AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and try again
    exit
fi


# for i in *_${datestamp}.json
# do
#     aws s3 cp $i s3://predict-mongodb/$i
# done

aws s3 cp . s3://predict-mongodb/ --recursive --exclude "*" --include "*_${datestamp}.json" --storage-class DEEP_ARCHIVE


