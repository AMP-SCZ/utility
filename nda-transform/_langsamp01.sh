#!/bin/bash

export PATH=/data/predict1/miniconda3/bin/:$PATH

_help()
{
    echo """Usage:
$0 TYPE DATA_FILE
$0 TYPE DATA_FILE submit

Accepted types are open or psychs only
Keep input data file within nda-submissions/langsamp01/ folder and provide basename
The keyword 'submit' is for submitting combined data to NDA
"""
    exit
}


if [ $# -lt 2 ] || [ "$1" == "-h" ]
then
    _help
fi


if [ "$1" == open ]
then
    prefix=chrspeech
    events="baseline month_2"
elif [ "$1" == psychs ]
then
    prefix=chrpsychs_av
    events="screening baseline month_1 month_2"
else
    _help
fi

data_file_suffix=$2


# generation
for n in Pronet Prescient
do
    echo $n
    for e in ${events}
    do
        echo $e
        ./generate.sh -f langsamp01 -n $n -e $e -p $prefix \
        -o "--data /data/predict1/to_nda/nda-submissions/langsamp01/${data_file_suffix}"
        echo
    done
done


# combination and validation
s=`echo "$1" | tr '[:upper:]' '[:lower:]'`
for e in ${events}
do
    echo $e
    ./combine_networks.sh -e $e -s $s -f langsamp01
    echo
done


if [ $# -eq 3 ] && [ "$2" == submit ]
then
    # submission
    for e in ${events}
    do
        ./submit.sh -e $e -s $s -f langsamp01 -u tbillah
        echo
    done
fi
