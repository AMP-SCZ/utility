#!/bin/bash

export PATH=/data/predict1/miniconda3/bin:$PATH

_help()
{
    echo """Usage:
./generate.sh -f nsipr -n Pronet -e baseline -p chrnsipr
./generate.sh -f assist01 -n Prescient -e month_2 -p chrassist

Mandatory:
-f : NDA dict name 
-n : network
-e : event
-p : variable name prefix e.g. chrnsipr, chrassist

Optional:
-d : name of interview date variable if it is not {prefix}_interview_date
"""

    exit
}


while getopts "f:n:e:p:d:" i
do
    case $i in
        f) form=$OPTARG ;;
        n) network=$OPTARG ;;
        e) event=$OPTARG ;;
        p) prefix=$OPTARG ;;
        d) idate=$OPTARG ;;
        ?) _help ;;
    esac
done

if [ -z $form ] || [ -z $network ] || [ -z $event ] || [ -z $prefix ]
then
    _help
fi

datestamp=$(date +"%Y%m%d")


pushd .
cd /data/predict1/to_nda/

if [ -z $idate ]
then

/data/predict1/utility/nda-transform/${form}.py --dict nda-templates/${form}_template.csv --root /data/predict1/data_from_nda/${network}/PHOENIX/GENERAL/ -t "*/processed/*/surveys/*.${network}.json" -o nda-submissions/${form}_${network}_${event}.csv --shared nda-submissions/ndar_subject01_${network}.csv -e ${event} -p $prefix

else

/data/predict1/utility/nda-transform/${form}.py --dict nda-templates/${form}_template.csv --root /data/predict1/data_from_nda/${network}/PHOENIX/GENERAL/ -t "*/processed/*/surveys/*.${network}.json" -o nda-submissions/${form}_${network}_${event}.csv --shared nda-submissions/ndar_subject01_${network}.csv -e ${event} -p $prefix --interview_date_var $idate


fi
popd

