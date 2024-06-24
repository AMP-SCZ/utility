#!/usr/bin/env bash

export PATH=/data/predict1/utility/:/data/predict1/miniconda3/bin/:$PATH
if [ -z $1 ] || [ ! -d $1 ]
then
    echo """$0 /path/to/nda_root/"""
    exit
else
    export NDA_ROOT=$1
fi


name='combined'
rm ${NDA_ROOT}/${name}_metadata.csv
rm ${NDA_ROOT}/Pronet_status/*csv
rm ${NDA_ROOT}/Prescient_status/*csv


for network in Pronet Prescient
do
    for timepoint in baseline month_2 month_6 month_12
    # for timepoint in baseline month_2 month_6 month_12 month_24
    do
        subject_files_status_for_dpdash2.py --network $network --timepoint $timepoint
    done
done

for visit in data_baseline data_month_2 data_month_6 data_month_12
# for visit in data_baseline data_month_2 data_month_6 data_month_12 data_month_24
do

    cd ${NDA_ROOT}/Pronet_status
    project_files_status_for_dpdash.py PRONET ../${name}_metadata.csv *-${visit}-day1to1.csv

    cd ${NDA_ROOT}/Prescient_status
    project_files_status_for_dpdash.py PRESCIENT ../${name}_metadata.csv *-${visit}-day1to1.csv
    
    cd ${NDA_ROOT}
    cat Pronet_status/${name}-PRONET-${visit}-day1to1.csv > ${name}-AMPSCZ-${visit}-day1to1.csv
    tail -n +2 Prescient_status/${name}-PRESCIENT-${visit}-day1to1.csv >> ${name}-AMPSCZ-${visit}-day1to1.csv
    renumber_days.py ${name}-AMPSCZ-${visit}-day1to1.csv

done

echo AMPSCZ,1,'-',${name} >> ${name}_metadata.csv


