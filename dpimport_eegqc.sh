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
--eval "assess=[\"EEGqc\",\"EEGquick\"]" /data/predict/utility/remove_assess.js
echo ''


# import new data
export PATH=/data/predict1/miniconda3/bin:$PATH

pushd .

cd $NDA_ROOT
FEATURE_DIR=${NDA_ROOT}/EEGqc_features
rm -f ${FEATURE_DIR}/*-day1to1.csv

out_template=${FEATURE_DIR}/combined-SITE-EEGqc-day1to1.csv
cd ${NDA_ROOT}/Pronet
/data/predict/utility/feature_combiner.py $out_template "./**/??-*-EEGqc-day1to*.csv"
cd ${NDA_ROOT}/Prescient
/data/predict/utility/feature_combiner.py $out_template "./**/??-*-EEGqc-day1to*.csv"

out_template=${FEATURE_DIR}/combined-SITE-EEGquick-day1to1.csv
cd ${NDA_ROOT}/Pronet
/data/predict/utility/feature_combiner.py $out_template "./**/??-*-EEGquick-day1to*.csv"
cd ${NDA_ROOT}/Prescient
/data/predict/utility/feature_combiner.py $out_template "./**/??-*-EEGquick-day1to*.csv"


cd ${NDA_ROOT}
for net in Pronet Prescient
do
    echo Combining $net features
    for d in `ls -d $net/PHOENIX/PROTECTED/${net}*`
    do
        echo Combining $d features
        pushd . > /dev/null
        cd $d
        /data/predict/utility/feature_combiner.py ${FEATURE_DIR}/combined-SITE-EEGqc-day1to1.csv "./**/??-*-EEGqc-day1to*.csv"
        /data/predict/utility/feature_combiner.py ${FEATURE_DIR}/combined-SITE-EEGquick-day1to1.csv "./**/??-*-EEGquick-day1to*.csv"
        popd > /dev/null
    done
done


# project level data
cd $FEATURE_DIR
import.py -c $CONFIG "*.csv"

popd

# subject level data
cd $NDA_ROOT
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/eeg/??-*-EEGqc-day1to*.csv"
import.py -c $CONFIG "*/PHOENIX/PROTECTED/*/processed/*/eeg/??-*-EEGquick-day1to*.csv"
