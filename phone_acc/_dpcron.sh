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
  phone:      phone_accel, phone_power, phone_survey, phone_survey_nda, data_availmg,
  actigraphy: geneactiv_extract_ax
  gps:        parse_gps_mc.py, preprocess_gps_mc, process_gps_mc, aggregate_gps_mc, phone_gps_mc


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


source ~/.bashrc
module load MATLAB/2019b
source /data/sbdp/dphtool/gps/bin/activate
export BEIWE_STUDY_PASSCODE='addle shindy winded subnormal'
# cd outerr


CONSENT_DIR=/data/predict1/data_from_nda/${network}/PHOENIX/PROTECTED
sitelist=${CONSENT_DIR}/dpcron-sites.txt
rm $sitelist

if [ -z $sites ]
then
    (cd $CONSENT_DIR && ls -d ${network}?? > $sitelist)
else
    for s in $(sites)
    do
        echo $s >> $sitelist
    done
fi


#BSUB dpcron[1-38]%4
#BSUB -q pri_pnl
#BSUB -o /data/predict1/utility/bsub/dpcron/dpcron-%J-%I.out
#BSUB -e /data/predict1/utility/bsub/dpcron/dpcron-%J-%I.err
#BSUB -R "span[hosts=1] order[!slots]"
#BSUB -n 2

if [ -z ${LSB_JOBINDEX} ]
then
    # must be a single case
    LSB_JOBINDEX=1
fi
p=`head -${LSB_JOBINDEX} ${sitelist} | tail -1`


if [ -z $modules ]
then

    # get module list from file
    modules=""
    for line in $(tail -n +2 exec-dtype.csv)
    do
        IFS=, read -a var <<< "$line"
        module=${var[0]}
        module=${module/.py/}
        module=`basename $module`
        modules="$modules $module"
    done

fi


for i in $modules
do

    # construct absolute path of the module
    for line in $(tail -n +2 exec-dtype.csv)
    do
        if [[ $line == *"$i"* ]]
        then
            IFS=, read -a var <<< "$line"
            exec=${var[0]}
            dtype=${var[1]}
            break
        fi
    done

    ls -la /data/sbdp/dphtool/$exec
    ls -ld `dirname $CONSENT_DIR`
    ls -ld `dirname /data/sbdp/dphtool/$exec`
    echo $dtype
    echo $i
    #/data/sbdp/dphtool/$exec --phoenix-dir `dirname $CONSENT_DIR` --consent-dir $CONSENT_DIR \
    #--matlab-dir `dirname /data/sbdp/dphtool/$exec` --study $p  --data-type $dtype --pipeline $i --include all \
    #--data-dir PROTECTED
done

rm $sitelist

