#!/bin/bash

cd /data/predict1/data_from_nda

for i in combined-AMPSCZ-data_*csv
do
    echo Uploading to Dropbox $i
    /data/predict1/dbxcli put $i ampscz-data-tracker/$i
done

