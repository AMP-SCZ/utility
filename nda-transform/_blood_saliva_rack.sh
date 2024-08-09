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


for n in Pronet
do
    for e in baseline month_2
    do

        echo $n $e
        /data/predict1/utility/nda-transform/blood_saliva_rack.py \
        --root /data/predict1/data_from_nda/${n}/PHOENIX/GENERAL/ \
        -o blood_saliva_rack_${n}_${e}.csv --shared ndar_subject01_${n}.csv \
        --template "*/processed/*/surveys/*.${n}.json" -e $e
        echo

    done


    combined=blood_saliva_rack_${n}.csv
    header=`head -n 1 blood_saliva_rack_${n}_${e}.csv`
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


cd fluid_shipment/

# count check
echo " Blood racks should have 96 entries"
echo "Saliva racks should have 48 entries"
echo
for i in *csv; do echo $i : `tail -n+2 $i | wc -l`; done

# combined manifest generation
datestamp=$(date +"%Y%m%d")
manifest=blood_saliva_rack_${datestamp}.csv
echo $header > $manifest
for i in *csv
do
    tail -n +2 $i >> $manifest
done

# create zip file for uploading to Dropbox
cd ..
echo
zip -r fluid_shipment_${datestamp}.zip fluid_shipment/

