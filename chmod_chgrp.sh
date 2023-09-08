#!/bin/bash


if [ $# -lt 1 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo """Script for setting g+s and changing group of directories
Usage:
$0 /data/predict1/data_from_nda/Pronet BWH-PREDICT-G
$0 /data/predict1/data_from_nda/Pronet
Default group is BWH-PREDICT-G"""
    exit
fi


if [ -z $2 ]
then
    g1=BWH-PREDICT-G
else
    g1=$2
fi

pushd .


echo Create list of directories under $1
cd $1
list=$(mktemp)
find . -type d > $list


echo Change permission of directories in $list
echo Not printing directory names for speed

IFS=$'\n'
for d in $(cat $list)
do
    g=`ls -ld ./PROTECTED/PronetYA/processed/YA11278/phone | cut -d ' ' -f 4`
    if [[ "$g" != "$g1" ]]
    then
        chgrp $g1 $d
    fi
    
    chmod g+s $d

done

popd

echo Done

