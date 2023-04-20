#!/bin/bash

if [ $# -lt 2 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]
then
    echo """Usage:
/path/to/utility/nda_s3_interact.sh \"*/raw/*/surveys/*_psychs_*_fu*csv\" ls
Run this script from PHOENIX/PROTECTED directory.
Source aws-keys before running it.
First arg is pattern, second arg is ls or rm"""
    exit
fi


if [ -z $AWS_ACCESS_KEY_ID ] || [ -z $AWS_SECRET_ACCESS_KEY ]
then
    echo Define AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and try again
    exit
fi


if [ $2 == 'ls' ]
then
    for i in $1
    do
        aws s3 ls s3://prescient-test/PHOENIX_ROOT_PRESCIENT/PROTECTED/$i
    done

elif [ $2 == 'rm' ]
then
    aws s3 rm --recursive --exclude "*" --include "PHOENIX_ROOT_PRESCIENT/PROTECTED/$1" s3://prescient-test
    rm $1
fi

