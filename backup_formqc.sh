#!/bin/bash

datestamp=$(date +"%Y%m%d")

cd /data/predict1/data_from_nda/

rm -rf `ls -d formqc.20* | head -n 1`

cp -a formqc/ formqc.$datestamp

