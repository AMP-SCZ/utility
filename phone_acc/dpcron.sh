#!/bin/bash


_help()
{
    echo """Usage:
$0 -n Pronet -m phone_accel -s PronetLA
$0 -n Pronet -m "phone_accel phone_power" -s "PronetLA PronetCA"

Mandatory:
-m : module name 
-n : network
-s : site name


modules are:
* If only -n is provided, site names are obtained automatically.
* Known modules are:
  phone:      "phone_accel phone_power phone_survey phone_survey_nda data_availmg"
  actigraphy: "geneactiv_extract_ax"
  gps:        "parse_gps_mc.py preprocess_gps_mc process_gps_mc aggregate_gps_mc phone_gps_mc"


"""

    exit
}


while getopts "m:n:s:" i
do
    case $i in
        m) modules=$OPTARG ;;
        n) network=$OPTARG ;;
        s) sites=$OPTARG ;;
        ?) _help ;;
    esac
done


if [ -z $network ]
then
    _help

fi


CONSENT_DIR=/data/predict1/data_from_nda/${network}/PHOENIX/PROTECTED
sitelist=${CONSENT_DIR}/dpcron-sites.txt
rm $sitelist

if [ -z "$sites" ]
then
    (cd $CONSENT_DIR && ls -d ${network}?? > $sitelist)
else
    for s in $sites
    do
        echo $s >> $sitelist
    done
fi

N=`cat $sitelist | wc -l`

source /etc/profile
# prevent getting thousand emails
export LSB_JOB_REPORT_MAIL=N

export network modules

bsub -J "dpcron[1-$N]%4" < /data/predict1/utility/phone_acc/dpcron.lsf

exit

# move bsub logs to a named folder
_bsub=dpcron-$(date +%Y%m%d)
cd /data/predict1/utility/bsub/dpcron
mkdir $_bsub
mv *err $_bsub/
mv *out $_bsub

