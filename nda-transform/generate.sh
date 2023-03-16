#!/bin/bash

export PATH=/data/predict1/miniconda3/bin:$PATH

_help()
{
    echo """Usage:
./generate.sh -f ndar_subject01 -n Pronet
./generate.sh -f ampscz_nsipr01 -n Pronet -e baseline -p chrnsipr
./generate.sh -f assist01 -n Prescient -e month_2 -p chrassist

Mandatory:
-f : NDA dict name 
-n : network
-e : event
-p : variable name prefix e.g. chrnsipr, chrassist

Optional:
-o : any optional arguments to pass to data generator e.g.
     \"--interview_date_var chrap_date\", \"--follow\"

ndar_subject01 is a special form that does not require -e and -p
"""

    exit
}


while getopts "f:n:e:p:o:" i
do
    case $i in
        f) form=$OPTARG ;;
        n) network=$OPTARG ;;
        e) event=$OPTARG ;;
        p) prefix=$OPTARG ;;
        o) optional=$OPTARG ;;
        ?) _help ;;
    esac
done


if [ $form == "ndar_subject01" ] && [ -z $network ]
then
    _help

elif [ $form != "ndar_subject01" ]
then
    if [ -z $network ] || [ -z $event ] || [ -z $prefix ]
    then
        _help
    fi
    
elif [ -z $form ]
then
    _help
fi


datestamp=$(date +"%Y%m%d")


pushd .
cd /data/predict1/to_nda/

if [ $form == "ndar_subject01" ]
then

cmd="/data/predict1/utility/nda-transform/${form}.py --dict nda-templates/${form}_template.csv --root /data/predict1/data_from_nda/${network}/PHOENIX/GENERAL/ -t "*/processed/*/surveys/*.${network}.json" -o nda-submissions/${form}_${network}.csv"

else

cmd="/data/predict1/utility/nda-transform/${form}.py --dict nda-templates/${form}_template.csv --root /data/predict1/data_from_nda/${network}/PHOENIX/GENERAL/ -t "*/processed/*/surveys/*.${network}.json" -o nda-submissions/${form}_${network}_${event}.csv --shared nda-submissions/ndar_subject01_${network}.csv -e ${event} -p $prefix $optional"

fi

echo $cmd
echo
$cmd

