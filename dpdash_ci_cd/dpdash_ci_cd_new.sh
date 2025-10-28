#!/bin/bash

# activate a proper Python environment for dpimport outside this script

# provides mongoimport
export PATH=~/Downloads/mongodb-database-tools-rhel93-x86_64-100.13.0/bin/:$PATH

# provides mongosh
~/Downloads/mongodb-mongosh-2.5.8.x86_64/usr/bin/:$PATH

# provides import.py
export PATH=~/Downloads/dpimport/scripts:$PATH

# data for initial configuration
# https://www.dropbox.com/scl/fo/vpgqohu7xijxc2fu73f1g/AJnc0t7K0YilXf-NkZpT4n0?rlkey=w9bph3ay8jt4alojgtv3euio2&st=x85z0tj5&dl=0
mongoimport --uri="mongodb://zhpysch18.mgb.org:27017/dpdmongo?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8" --collection=charts charts_20250815.json
mongoimport --uri="mongodb://zhpysch18.mgb.org:27017/dpdmongo?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8" --collection=users users_20250815.json
mongoimport --uri="mongodb://zhpysch18.mgb.org:27017/dpdmongo?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8" --collection=configs configs_20250815.json

# data from charts
cd /data/predict1/data_from_nda/
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_informed_consent_run_sheet-day1to*.csv" && \
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_inclusionexclusion_criteria_review-day1to*.csv" && \
import.py -c $CONFIG "Pr*/PHOENIX/PROTECTED/Pr*/processed/*/surveys/??-*-form_sociodemographics-day1to*.csv" && \
import.py -c $CONFIG "formsdb/dpdash-recruit-filter/??-*-form_filters-day1to1.csv"

# data for files status
import.py -c $CONFIG combined_metadata.csv && \
import.py -c $CONFIG "*_status/??-*-data_*-day1to1.csv" && \
import.py -c $CONFIG "*_status/combined-??-data_*-day1to1.csv"

# login and do whatever
mongosh "mongodb://zhpysch18.mgb.org:27017/dpdmongo?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.8"

