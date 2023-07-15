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

# run the combining step outside this script
#
# network level combination of family members
# ./combine_networks -f figs01 -e screening -n $1
#
# project level combination
# ./combine_networks -f figs01 -e screening

