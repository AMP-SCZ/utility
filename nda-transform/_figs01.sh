#!/bin/bash

if [ $# -lt 1 ]
then
    echo Usage: $0 Pronet/Prescient
    exit
fi

for m in mother father sibling1 sibling2 sibling3 sibling4 sibling5 sibling6 sibling7 sibling8 sibling9 child1 child2 child3 child4
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

