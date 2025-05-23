#!/bin/bash


_help()
{
    echo """Usage:
$0 -n Pronet -m phone_accel -s PronetLA
$0 -n Pronet -m \"phone_accel phone_power\" -s \"PronetLA PronetCA\"

Mandatory:
-n : network

Optional:
-m : module name(s)
-s : site name(s)


* If only -n is provided, site names are obtained automatically.
* Known modules are:
  phone:      \"phone_accel phone_power phone_survey phone_survey_nda data_availmg\"
  actigraphy: \"geneactiv_extract_ax geneactiv_freq geneactiv_act geneactiv_sync_mc geneactiv_qcact geneactiv_upact\"
  gps:        \"parse_gps_mc preprocess_gps_mc process_gps_mc aggregate_gps_mc phone_gps_mc\"


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

# source /etc/profile
# prevent getting thousand emails
# export LSB_JOB_REPORT_MAIL=N

export network modules

LOGDIR=/data/predict1/utility/slurm/dpcron/
mkdir -p $LOGDIR

sbatch -a 1-$N%6 < /data/predict1/utility/phone_act/_dpcron.slurm


# move bsub logs to a named folder
_bsub=dpcron-${network}-$(date +%Y%m%d)
cd $LOGDIR
mkdir -p $_bsub
while [ 1 ]
do
    count=`ls *out | wc -l`
    if [ $count -lt $N ]
    then
        sleep 60
    else
        mv *err $_bsub/
        mv *out $_bsub/
        break
    fi
done

