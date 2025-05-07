#!/bin/bash

# this wrapper script is essential because #BSUB -J redcap-import[1-$N]
# is not allowed within records_to_redcap.lsf

if [ $# -lt 3 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo """Usage:
./_records_to_redcap.sh /path/to/PHOENIX/PROTECTED/ /redcap/dict/dir/ API_TOKEN"""
    exit 1
fi

redcap_records=/data/predict1/utility/slurm/redcap_records.txt
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
ls */raw/*/surveys/*.Pronet.json > $redcap_records
N=`cat $redcap_records | wc -l`

batch=200
duration=3600
for (( i=1; i<=N; i+=$batch ))
do

    if [[ $(( i+$batch )) -lt $N ]]
    then
        max=$(( i+$batch-1 ))
    else
        max=$N
    fi
    
    echo [$i-$max]
    sbatch -a $i-$max%12 < /data/predict1/utility/records_to_redcap.lsf
    # wait between consecutive batch of jobs so the previous one can complete
    sleep $duration
    
done



# move slurm logs to a named folder
_bsub=pronet-$(date +%Y%m%d)
cd /data/predict1/utility/slurm/
mkdir $_bsub
mv *err $_bsub/
mv *out $_bsub/

