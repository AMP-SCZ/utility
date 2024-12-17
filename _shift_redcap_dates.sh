#!/bin/bash

export OPENBLAS_NUM_THREADS=16

export PATH=/data/predict1/miniconda3/bin:$PATH

PHOENIX_PROTECTED=$1
JSON=$2

cd /data/predict1/utility/
./set_date_shifts.py $PHOENIX_PROTECTED $JSON
./shift_redcap_dates.py $PHOENIX_PROTECTED $JSON $3

# explicit permission change
chgrp BWH-PREDICT-G ${PHOENIX_PROTECTED/PROTECTED/GENERAL}/Pronet??/processed/*/surveys/
chmod g+w ${PHOENIX_PROTECTED/PROTECTED/GENERAL}/Pronet??/processed/*/surveys/
chgrp BWH-PREDICT-G ${PHOENIX_PROTECTED/PROTECTED/GENERAL}/Pronet??/processed/*/surveys/???????.Pronet.json

