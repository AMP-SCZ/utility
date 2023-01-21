#!/bin/bash

    if [ $# -lt 2 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]
    then
        echo """Usage:
./nda_s3_interact.sh "*/raw/*/surveys/*_psychs_*_fu*csv" ls
Run this script from PHOENIX/PROTECTED directory.
Source aws-keys before running it.
First arg is pattern, second arg is ls or rm"""
        exit
    fi

for i in $1
do
    aws s3 $2 s3://prescient-test/PHOENIX_ROOT_PRESCIENT/PROTECTED/$i
    rm $i
done

