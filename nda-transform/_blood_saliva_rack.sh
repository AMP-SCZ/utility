#!/bin/bash


if [ "$1" == "-h" ]
then

    echo """Usage:
To generate list of all racks:
$0
To generate list of individual racks:
$0 123456 ProNET-1234"""
    exit

fi

cd /data/predict1/to_nda/nda-submissions/
header="Rack Code,Position on Rack,Draw Date,Inventory Code,Matcode,AMPSCZ_ID,Cohort,Sex,Age on Draw Date,Age Unit,GUID"


for n in Pronet
do
    for e in baseline month_2
    do

        echo $n $e
        /data/predict1/utility/nda-transform/blood_saliva_rack.py \
        --root /data/predict1/data_from_nda/${n}/PHOENIX/PROTECTED/ \
        -o blood_saliva_rack_${n}_${e}.csv --shared ndar_subject01_${n}.csv \
        --template "*/raw/*/surveys/*.${n}.json" -e $e
        echo

    done


    combined=blood_saliva_rack_${n}.csv
    echo $header > $combined
    for f in blood_saliva_rack_${n}_baseline.csv blood_saliva_rack_${n}_month_2.csv
    do
        tail -n +2 $f >> $combined
    done
    
    
done



# filter the above by a rack code
if [ ! -z  $1 ]
then
    for code in "$@"
        do
            
            assorted=fluid_shipment/blood_saliva_rack_${code}.csv
            echo $header > $assorted
            grep ^$code, blood_saliva_rack_Pronet.csv >> $assorted
            # grep ^$code, blood_saliva_rack_Prescient.csv >> $assorted
            
            echo Generated $assorted
            echo
        done

fi


