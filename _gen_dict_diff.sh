#!/bin/bash

export PATH=/data/predict1/miniconda3/bin/:$PATH
cd /data/predict/utility/dict_diff
CURL=`which curl`
datestamp=$(date +"%Y%m%d")

# download ground truth dictionary
ampscz=ampscz/ampscz_dict_${datestamp}.csv
DATA="token=${1}&content=metadata&format=csv&returnFormat=json"
$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      https://redcap.partners.org/redcap/api/ > $ampscz


# download pronet dictionary
pronet=pronet/pronet_dict_${datestamp}.csv
: << CMT
DATA="token=${2}&content=metadata&format=csv&returnFormat=json"
$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      https://redcap.partners.org/redcap/api/ > $pronet
CMT
cp /data/predict1/data_from_nda/Pronet/PHOENIX/GENERAL/redcap_metadata.csv $pronet


# download prescient dictionary
prescient=prescient/prescient_dict_${datestamp}.csv
DATA="token=${3}&content=metadata&format=csv&returnFormat=json"
$CURL -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Accept: application/json" \
      -X POST \
      -d $DATA \
      https://redcap.partners.org/redcap/api/ > $prescient


for net in pronet prescient
do
    /data/predict/utility/gen_dict_diff.py $ampscz ${net}/${net}_dict_${datestamp}.csv $net
    suffix=${net}_${datestamp}

    # email report
    for p in ${@: 4:$#}
    do

        echo "" | mailx -s diff_ampscz_${suffix} \
        -a ampscz_vars_absent_in_${suffix}.csv \
        -a branch_logic_diff_ampscz_${suffix}.csv \
        -a calc_diff_ampscz_${suffix}.csv \
        -- ${p}@partners.org

    done
done


# backup the ampscz and pronet dictionaries
source /data/pnl/soft/pnlpipe3/duply_backup/env.sh
duply /data/pnl/soft/pnlpipe3/duply_backup/duply_profile/amp-scz-data-dicts backup

