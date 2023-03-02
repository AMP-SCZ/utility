#!/bin/bash

export OPENBLAS_NUM_THREADS=16

export PATH=/data/predict1/miniconda3/bin:$PATH

PHOENIX_PROTECTED=$1
JSON=$2

cd /data/predict1/utility/
./set_date_shifts.py $PHOENIX_PROTECTED $JSON
./shift_redcap_dates.py $PHOENIX_PROTECTED $JSON $3


