#!/bin/bash

_help()
{
    echo """Usage:
$0 -n Pronet -s LA -c \"7000432738 3000917468 3000704241\"

Mandatory:
-n : network
-s : two-letter upper case site code
-c : rack codes enclosed in double quotes, separated by space
"""

    exit
}


while getopts "n:s:c:" i
do
    case $i in
        n) network=$OPTARG ;;
        s) site=$OPTARG ;;
        c) racks=$OPTARG ;;
        ?) _help ;;
    esac
done

if [ -z $network ] || [ -z $site ] || [ -z "$racks" ]
then
    _help
fi



cd /data/predict1/to_nda/nda-submissions/

combined=blood_saliva_rack_${network}.csv
header=`head -n 1 blood_saliva_rack_${network}.csv`

mv fluid_shipment fluid_shipment.$(date +"%Y%m%d-%H%M")
mkdir fluid_shipment
for code in $racks
do
    assorted=fluid_shipment/blood_saliva_rack_${code}.csv
    echo $header > $assorted
    grep ^$code, blood_saliva_rack_${network}.csv >> $assorted

    echo Generated $assorted
    echo
done


cd fluid_shipment/

# count check
echo " Blood racks should have 96 entries"
echo "Saliva racks should have 48 entries"
echo
for i in *csv; do echo $i : `tail -n+2 $i | wc -l`; done


# upload to Dropbox
for i in *csv
do
    name=${site}_${i}
    mv $i $name
    dbxcli put $name blood_saliva_manifests/$name
done

