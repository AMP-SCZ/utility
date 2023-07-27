#!/bin/bash


cd /data/predict1/to_nda/nda-submissions/

header="Rack Code,Position on Rack,Draw Date,Inventory Code,Matcode,AMPSCZ_ID,Cohort,Sex,Age on Draw Date,Age Unit,GUID"

for n in Pronet
do
    for e in baseline month_2
    do
    
        /data/predict1/utility/nda-transform/blood_saliva_rack.py \
        --root /data/predict1/data_from_nda/${n}/PHOENIX/PROTECTED/ \
        -o blood_saliva_rack_${n}_${e}.csv --shared ndar_subject01_${n}.csv \
        --template "*/raw/*/surveys/*.${n}.json" -e $e
        
    done


    combined=blood_saliva_rack_${n}.csv
    echo $header > $combined
    for f in blood_saliva_rack_${n}_baseline.csv blood_saliva_rack_${n}_month_2.csv
    do
        tail -n +2 $f >> $combined
    done
    
    
done

exit
# filter the above by a rack code
if [ ! -z  $1 ]
then
    echo $header > blood_saliva_rack_${1}.csv
    grep ^$1, blood_saliva_rack_*csv >> blood_saliva_rack_${1}.csv
fi


