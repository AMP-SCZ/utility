#!/bin/bash

    if [ $# -lt 2 ] || [ $1 == "-h" ] || [ $1 == "--help" ]
    then
        echo """Convenience script for backing up network's data
Usage:
$0 Prescient /data/predict1/archive/release-4-prescient.bak
$0 Pronet /data/predict1/archive/release-4-pronet.bak"""
        exit
    fi


NET=$1
ARCHIVE=$2

datestamp=$(date +"%Y%m%d")

mkdir -p $ARCHIVE/raw
mkdir -p $ARCHIVE/processed

############################################

cd /data/predict1/data_from_nda/${NET}/PHOENIX/PROTECTED

# raw JSONs
zip $ARCHIVE/raw/${NET}-PROTECTED.json.${datestamp}.zip -r ${NET}??/raw/*/surveys/*.${NET}.json

# raw surveys
if [ ${NET} == Prescient ]
then
    for site in ${NET}??; do pushd .; cd ${site}/raw; for s in ???????; do echo $s; zip $ARCHIVE/raw/${s}.surveys.zip -r ${s}/surveys/${s}_*.csv; done; popd; done
fi

############################################

cd /data/predict1/data_from_nda/${NET}/PHOENIX/GENERAL

# shifted JSONs
zip $ARCHIVE/processed/${NET}-GENERAL.json.${datestamp}.zip -r ${NET}??/processed/*/surveys/*.${NET}.json

# processed outcomes
for site in ${NET}??; do pushd .; cd ${site}/processed/; for s in ???????; do echo $s; zip $ARCHIVE/processed/${s}.outcomes.zip -q -r ${s}/surveys/*.csv; done; popd; done


