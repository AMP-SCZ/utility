#!/bin/bash

export PATH=/data/predict1/miniconda3/bin:$PATH

_help()
{
    echo """Usage:
./submit.sh -u tashrif -f ndar_subject01 -n Pronet -e baseline
./submit.sh -u tashrif -f ndar_subject01 -n Prescient
./submit.sh -u tashrif -f ndar_subject01
./submit.sh -f ndar_subject01

Mandatory:
-f : NDA dict name 

Optional:
-u : submitter's NDA username
-n : network
-e : event

nda-submission directory is globed for \${f}_\${n}_\${e}.csv to find files to submit
do not provide -u for only validation
"""

    exit
}


while getopts "u:f:n:e:" i
do
    case $i in
        u) user=$OPTARG ;;
        f) form=$OPTARG ;;
        n) network=$OPTARG ;;
        e) event=$OPTARG ;;
        ?) _help ;;
    esac
done

if [ -z $form ]
then
    _help
fi


collection=PROD-AMPSCZ
root=/data/predict1
datestamp=$(date +"%Y%m%d")


# look for existing submission ID
idline=`grep "$form,$event," $root/utility/nda-transform/submission_ids.csv`
IFS=, read -ra idarray <<< "$idline"
id=${idarray[2]}
echo $id

for data in `ls $root/to_nda/nda-submissions/network_combined/${form}*${network}*${event}.csv`
do
    echo Processing $data

    if [ -z $user ]
    then
        # validate only
        python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
        $data

    else
        # validate and submit
        title=`basename ${data/.csv/}`

        if [ -z $id ]
        then
            python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
            -u $user -t $title -d $title \
            -a $collection \
            -b $data
        else
            # -t and -d are disallowed with --replace-submission
            python $root/nda-tools/NDATools/clientscripts/vtcmd.py \
            -u $user \
            -a $collection \
            --replace-submission $id \
            -b $data
        fi

        
    fi

    echo ''
    # the wait maybe useful
    sleep 15
done


