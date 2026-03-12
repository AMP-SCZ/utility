#!/bin/bash

if [ "$1" == "-h" ] || [ $# == 0 ] 
then
    echo """Usage:
$0 REFERENCE TARGET
Lines from REFERENCE file will be searched in and removed from TARGET file.
"""
    exit
fi

REFERENCE=$1
TARGET=$2

echo "Duplicate lines:"
echo

for i in $(tail -n+2 $REFERENCE)
do
    match=`grep $i $TARGET`
    if [ ! -z $match ]
    then
        echo $i
        sed -i "\+$i+d" $TARGET
    fi
done

