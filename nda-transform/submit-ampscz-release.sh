#!/bin/bash

set -e

pushd .

cd /data/predict1/to_nda/nda-submissions/network_combined/

# public collection
python /data/predict1/nda-tools/NDATools/clientscripts/vtcmd.py -d ampscz-release-1.0 -t ampscz-release-1.0 -c 3705 -u tbillah -f \
langsamp01_baseline_open.csv image03_baseline.csv ampscz_sp_survey01.csv assist01_baseline.csv ampscz_iqa01_baseline.csv wasi201_baseline.csv wisc_v01_baseline.csv actirec01.csv ampscz_sp_sensors01_3705.csv eeg_sub_files01_baseline.csv socdem01.csv ampscz_psychs01_baseline.csv ampscz_nsipr01_baseline.csv ampscz_pps01_baseline.csv bprs01_baseline.csv clgry01_baseline.csv cssrs01_baseline.csv oasis01_baseline.csv pmod01_baseline.csv sri01_baseline.csv pss01_baseline.csv ampscz_rap01_baseline.csv ampscz_hcgfb01_screening.csv ampscz_lapes01_screening.csv scidvapd01_screening.csv tbi01_screening.csv dsm_iv_es01_screening.csv ampscz_psychs01_screening.csv ampscz_dim01.csv ampscz_rs01.csv iec01.csv pds01.csv figs01.csv wais_iv_part101_baseline.csv gfs01_chrgfss.csv gfs01_chrgfrs.csv ndar_subject01.csv dsm_iv_es01_baseline.csv cgis01_baseline.csv -b
# use -l . to avoid prompt for associated files' directory

# private collection
python /data/predict1/nda-tools/NDATools/clientscripts/vtcmd.py -d ampscz-release-1.0 -t ampscz-release-1.0 -c 4366 -u tbillah -f \
ndar_subject01.csv ampscz_sp_sensors01_4366.csv -b

popd

