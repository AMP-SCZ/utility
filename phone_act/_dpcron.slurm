#!/bin/bash

#SBATCH -p normal
#SBATCH -o /data/predict1/utility/slurm/dpcron/dpcron-%N-%j-%a.out
#SBATCH -e /data/predict1/utility/slurm/dpcron/dpcron-%N-%j-%a.err
#SBATCH --mem 8000
#SBATCH -t 0-48:00
#SBATCH -c 2


source ~/.bashrc
module load MATLAB/2019b
source /data/sbdp/dphtool/gps/bin/activate
export BEIWE_STUDY_PASSCODE='addle shindy winded subnormal'


CONSENT_DIR=/data/predict1/data_from_nda/${network}/PHOENIX/PROTECTED
sitelist=${CONSENT_DIR}/dpcron-sites.txt


p=`head -${SLURM_ARRAY_TASK_ID} ${sitelist} | tail -1`


EXEC=/data/predict1/utility/phone_act/exec-dtype.csv

if [ -z "$modules" ]
then

    # get module list from file
    modules=""
    for line in $(tail -n +2 $EXEC)
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
    for line in $(tail -n +2 $EXEC)
    do
        if [[ $line == *"/$i"* ]]
        then
            IFS=, read -a var <<< "$line"
            exec=${var[0]}
            dtype=${var[1]}
            break
        fi
    done

    cmd="/data/sbdp/dphtool/$exec --phoenix-dir `dirname $CONSENT_DIR` --consent-dir $CONSENT_DIR \
        --matlab-dir `dirname /data/sbdp/dphtool/$exec` --study $p  --data-type $dtype --pipeline $i --include all \
        --data-dir PROTECTED"
    echo $cmd
    echo
    $cmd
    
done

