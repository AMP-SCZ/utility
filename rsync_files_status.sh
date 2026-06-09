#!/bin/bash

export LD_LIBRARY_PATH=/apps/software/librsync/2.3.4-GCCcore-13.3.0/lib:$LD_LIBRARY_PATH
export PATH=/apps/software/rsync/3.4.1-GCCcore-13.3.0/bin:$PATH

rsync -avR -O --no-perms /data/predict1/data_from_nda/combined-*-data_*-day1to1.csv zhpysch13.mgb.org:/
rsync -avR -O --no-perms /data/predict1/data_from_nda/Pronet_status/combined-*-data_*-day1to1.csv zhpysch13.mgb.org:/
rsync -avR -O --no-perms /data/predict1/data_from_nda/Prescient_status/combined-*-data_*-day1to1.csv zhpysch13.mgb.org:/

