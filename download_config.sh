#!/usr/bin/env bash

if [[ $# -lt 2 ]]
then
    echo "Usage: ./download_config.sh config_name /tmp/config_name.json"
    echo "Provide configuration name and output file name"
    exit 1
fi

export state=""
export MONGO_PASS=""
export GODEBUG=x509ignoreCN=0

tmpJson=/tmp/config_`pgrep -f $0`.json
scriptDir=`dirname $0`

# export from mongodb
mongoexport --ssl --sslCAFile=$state/ssl/ca/cacert.pem --sslPEMKeyFile=$state/ssl/mongo_client.pem --uri="mongodb://dpdash:$MONGO_PASS@`hostname`:27017/dpdmongo?authSource=admin" --collection=configs --query="{\"name\":\"$1\"}" --out=$tmpJson && \
# modify according to https://github.com/AMP-SCZ/dpdash/wiki/Configuration-schema
$scriptDir/_download_config.py $tmpJson $2

rm $tmpJson

