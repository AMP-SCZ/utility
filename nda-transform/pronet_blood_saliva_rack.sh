#!/bin/bash

# This semi-automated script serves both as a script and a documentation for generating blood_saliva manifests.

export PATH=/data/predict1/miniconda3/bin/:$PATH


# Step-1 (optional)
# shift all raw data for confidence
# uncomment the shifter as needed
cd /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED
# /data/predict1/utility/set_date_shifts.py . "*/raw/*/surveys/*.Pronet.json"
# /data/predict1/utility/shift_redcap_dates.py . "*/raw/*/surveys/*.Pronet.json" /data/predict1/utility/yale-real/CloneOfYaleRealRecords_DataDictionary_2025-02-24.csv 8 1


# Step-2
# generate ndar_subject01.csv
cd /data/predict1/utility/nda-transform/
./generate.sh -f ndar_subject01 -n Pronet


# Step-3
# generate blood_saliva_rack_Pronet.csv
./_blood_saliva_rack.sh


# Step-4 (optional)
# generate the commands for Step-5 from email body
# ./_sort_blood_saliva_rack.py ...


# Step-5
# generate the actual manifests and upload to Dropbox
# ./sort_blood_saliva_rack.sh ...

: << NOTE

* New manifests are stored in `/data/predict1/to_nda/nda-submissions/fluid_shipment`
while previous manifests are backed up in `fluid_shipment.${datestamp}` folder.

* Go to `https://www.dropbox.com/home/Tashrif%20Billah/blood_saliva_manifests` and confirm
availability of the new manifests. If a manifest has not changed since last time it was
uploaded, it will not be re-uploaded. You can observe this subtlety by checking the
`Modified` column.

NOTE
