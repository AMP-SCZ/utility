#!/bin/bash

if [ $# -lt 1 ]
then
    echo Usage: $0 baseline/month_1/month_2/...
    exit
fi

event=$1

if $event=='baseline'
then
    prefixes="chrgfss chrgfrs"
else
    prefixes="chrgfssfu chrgfrsfu"
fi

for p in $prefixes
do

    echo
    echo Generation step
    echo

    for n in Pronet Prescient
    do
        cmd="./generate.sh -f gfs01 -n $n -e $event -p $p"
        echo $cmd
        echo
        $cmd
        echo
    done
    
    echo Combining step
    cmd="./combine_networks.sh -f gfs01 -e $event -s $p"
    echo $cmd
    $cmd
    echo

done

