#!/bin/bash

# this wrapper script is essential because #BSUB -J redcap-import[1-$N]
# is not allowed within records_to_redcap.lsf

if [ $# -lt 3 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo """Usage:
./_rpms_to_redcap.sh /path/to/PHOENIX/PROTECTED/ /redcap/dict/dir/ API_TOKEN"""
    exit 1
fi

redcap_records=/data/predict1/utility/slurm/rpms_records.txt
redcap_phoenix=$1
redcap_dict=$2
API_TOKEN=$3
FORCE=0
export redcap_records redcap_phoenix redcap_dict API_TOKEN FORCE
# export is to allow them to be used within records_to_redcap.lsf

# echo 'Deleting old records ...'
export PATH=/data/predict1/miniconda3/bin/:$PATH
# /data/predict1/utility/delete_redcap_records.py $redcap_phoenix $API_TOKEN

echo  'Uploading new records ...'
cd $redcap_phoenix
if [ -f rpms_records.txt ]
then
    # rpms_records.txt should consist of selective records
    # instead of all records under $redcap_phoenix
    redcap_records=${redcap_phoenix}/rpms_records.txt
else
    ls -d Prescient??/raw/*/surveys > $redcap_records
fi

N=`cat $redcap_records | wc -l`

batch=12
duration=300
for (( i=1; i<=$N; i+=1 ))
do

    echo $i
    export SLURM_ARRAY_TASK_ID=$i
    bash /data/predict1/utility/rpms_to_redcap.lsf &
    # wait between consecutive batch of jobs so the previous one can complete
    if [ $(( $i % $batch )) -eq 0 ] || [ $i -eq $N ]
    then
        while [ 1 ]
        do
            active=`ps aux | grep "[/]data/predict1/utility/rpms_to_redcap.lsf"`
            if [ ! -z "$active" ]
            then
                sleep 60
            else
                break
            fi
        done
    fi

done



# move slurm logs to a named folder
_bsub=prescient-$(date +%Y%m%d)
cd /data/predict1/utility/slurm/
mkdir -p $_bsub
mv *err $_bsub/
mv *out $_bsub/

