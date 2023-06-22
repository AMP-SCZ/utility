#!/bin/bash

if [ $# -lt 1 ]
then
    echo Usage: $0 /path/to/wisc_v01_*csv
    exit
fi

newfile=${1/wisc_v/wais_iv_part1}

sed "s/wisc_v/wais_iv_part1/g" $1 > $newfile

