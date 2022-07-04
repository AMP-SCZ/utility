#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_eegqc.sh /path/to/nda_root/ VM
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
--eval "assess=[\"EEGqc\"]" /data/predict/utility/remove_assess.js
echo ''


# import new data
source /data/predict/miniconda3/bin/activate base && conda activate dpimport

pushd .

cd $NDA_ROOT
FEATURE_DIR=${NDA_ROOT}/EEGqc_features
rm -f ${FEATURE_DIR}/*-day1to1.csv
out_template=${FEATURE_DIR}/combined-SITE-EEGqc-day1to1.csv

cd ${NDA_ROOT}/Pronet
/data/predict/utility/feature_combiner.py $out_template
cd ${NDA_ROOT}/Prescient
/data/predict/utility/feature_combiner.py $out_template

cd ${NDA_ROOT}
for net in Pronet Prescient
do
    echo Combining $net features
    for d in `ls -d $net/PHOENIX/PROTECTED/${net}*`
    do
        echo Combining $d features
        pushd . > /dev/null
        cd $d
        /data/predict/utility/feature_combiner.py $out_template
        popd > /dev/null
    done
done


cd $FEATURE_DIR
import.py -c /data/predict/dpimport/examples/$CONFIG "*.csv"

popd


