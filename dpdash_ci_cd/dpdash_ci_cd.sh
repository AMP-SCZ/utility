#!/bin/bash


_HOST=rc-predict-dev

# copy Mongo SSL keys
cd /data/predict1/rc-predict-dev-mongo-keys
rm -rf ssl
scp -r rc-predict-dev.partners.org:/opt/dpdash/dpstate/ssl .
echo Update the MongoDB password in .vault/.env.$_HOST
echo and in /data/predict1/dpimport/examples/config.yml.$_HOST


# import collections
cd /data/predict1/utility/
source .vault/.env.$_HOST
cd dpdash_ci_cd/

export PATH=/data/predict1/mongodb-database-tools-rhel70-x86_64-100.5.2/bin/:$PATH
export GODEBUG=x509ignoreCN=0

# import charts
mongoimport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdata?authSource=admin" --collection charts --maintainInsertionOrder --file=charts_20230728_ci_cd.json

# import configs
mongoimport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdmongo?authSource=admin" --collection configs --maintainInsertionOrder --file=configs_20230728_ci_cd.json

# import users
mongoimport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@$HOST:$PORT/dpdmongo?authSource=admin" --collection users --maintainInsertionOrder --file=users_20230728_ci_cd.json

# import data
export PATH=/data/predict1/miniconda3/bin/:$PATH

# formqc, only visit status chart data
cd /data/predict1/data_from_nda/formqc/
import.py -c $CONFIG "??-*-form_inclusionexclusion_criteria_review-day1to*.csv"
import.py -c $CONFIG "??-*-form_sociodemographics-day1to*.csv"
import.py -c $CONFIG "??-*-form_informed_consent_run_sheet-day1to*.csv"

# data flow, all data
/data/predict1/utility/dpimport_files_status.sh /data/predict1/data_from_nda/ $HOST

