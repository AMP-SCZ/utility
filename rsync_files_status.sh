#!/bin/bash

rsync -avR /data/predict1/data_from_nda/combined-*-data_*-day1to1.csv rc-predict-dev.partners.org:/
rsync -avR /data/predict1/data_from_nda/Pronet_status/combined-*-data_*-day1to1.csv rc-predict-dev.partners.org:/
rsync -avR /data/predict1/data_from_nda/Prescient_status/combined-*-data_*-day1to1.csv rc-predict-dev.partners.org:/

