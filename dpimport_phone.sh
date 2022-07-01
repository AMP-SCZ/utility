#!/usr/bin/env bash

export PATH=/data/predict/mongodb-linux-x86_64-rhel70-4.4.6/bin:$PATH

if [ -z $1 ] || [ ! -d $1 ]
then
    echo """./dpimport_phone.sh /path/to/nda_root/ VM
Provide /path/to/nda_root/ and VM
VM name examples:
    dpstage for dpstage.dipr.partners.org
    rc-predict for rc-predict.bwh.harvard.edu
    rc-predict-dev for rc-predict-dev.bwh.harvard.edu
    It is the first part of the server name."""
    exit
else
    export NDA_ROOT=$1
fi

source /data/predict/utility/.vault/.env.${2}


# import new data
source /data/predict/miniconda3/bin/activate base
cd ${NDA_ROOT}
import.py -c /data/predict/dpimport/examples/$CONFIG "*/PHOENIX/PROTECTED/*/processed/*/phone/*/*.csv"
import.py -c /data/predict/dpimport/examples/$CONFIG "*/PHOENIX/PROTECTED/*/processed/*/actigraphy/*/*.csv"


