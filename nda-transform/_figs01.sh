#!/bin/bash

if [ $# -lt 1 ]
then
    echo Usage: $0 Pronet/Prescient
    exit
fi

for m in father mother sibling children
do
    ./generate.sh -f figs01 -n $1 -p chrfigs -e screening -o "--member $m"
done

./combine_networks -f figs01 -e screening

