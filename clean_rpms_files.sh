#!/bin/bash

if [ $# -lt 1 ] || [ $1 == '-h' ] || [ $1 == '--help' ]
then
    echo """Convenience script for cleaning RPMS survey files.
It is useful to clean up when unprocessed data get routed through NDA cloud to DPACC.
Usage:
$0 value
Accepted values are:
    - for PRESCIENT side: /var/lib/prescient/data/PHOENIX/PROTECTED
    - for DPACC side: /data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED"""

    exit
fi

ROOT=$1

echo PrescientME
cd $ROOT/PrescientME/raw
for i in {0..9}; do echo $i; rm -f ME${i}*/surveys/*csv; done

cd $ROOT
for s in Prescient??; do echo $s; rm -f $s/raw/???????/surveys/*csv; done

