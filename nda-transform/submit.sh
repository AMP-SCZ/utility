#!/bin/bash

export PATH=/data/predict1/miniconda3/bin:$PATH

_help()
{
    echo """Usage:
./submit.sh -u tashrif -f ndar_subject01 -n Pronet -e baseline
./submit.sh -u tashrif -f ndar_subject01 -n Prescient
./submit.sh -u tashrif -f ndar_subject01
./submit.sh -f ndar_subject01
./submit.sh -f langsamp01 -e baseline -s open

Mandatory:
-f : NDA dict name 

Optional:
-u : submitter's NDA username
-n : network
-e : event
-s : suffix
-c : collection

nda-submission directory is globed for \${f}_\${n}_\${e}_\${s}.csv to find files to submit
to only validate, do not provide -u
default collection is 3705, private collection is 4366
"""

    exit
}


while getopts "u:f:n:e:c:s:" i
do
    case $i in
        u) user=$OPTARG ;;
        f) form=$OPTARG ;;
        n) network=$OPTARG ;;
        e) event=$OPTARG ;;
        c) collection=$OPTARG ;;
        s) suffix=$OPTARG ;;
        ?) _help ;;
    esac
done

if [ -z $form ]
then
    _help
fi


# collection=PROD-AMPSCZ
if [ -z $collection ]
then
    collection=3705
fi
# Personal Tracking Device data are collected at 4366

root=/data/predict1
datestamp=$(date +"%Y%m%d")


# look for existing submission ID
if [ -z $suffix ]
then
    event1=$event
else
    event1=${event}_${suffix}
fi

idline=`grep "$form,$event1," $root/utility/nda-transform/submission_ids.csv`
IFS=, read -ra idarray <<< "$idline"
id=${idarray[2]}
echo $id

pushd .
cd $root/to_nda/nda-submissions/network_combined/

for data in `ls ${form}*${network}*${event}*${suffix}.csv`
do
    echo Processing $data

    if [ -z $user ]
    then
        # validate only
        vtcmd \
        $data

    else
        # validate and submit
        title=`basename ${data/.csv/}`

        if [ -z $id ]
        then
            vtcmd \
            -u $user -t $title -d $title \
            -c $collection \
            -l . \
            -b $data
        else
            # -t and -d are disallowed with --replace-submission
            vtcmd \
            -u $user \
            --replace-submission $id \
            -f \
            -l . \
            -b $data
        fi

        
    fi

    echo ''
    # the wait maybe useful
    sleep 15
done

popd

