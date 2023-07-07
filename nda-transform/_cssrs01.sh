#!/bin/bash

if [ "$1" == "-h" ]
then
    echo Usage: $0
    exit
fi


for e in baseline month_2
do

    if [ $e == baseline ]
    then
        pre=chrcssrsb
    else
        pre=chrcssrsfu
    fi

    for n in Pronet Prescient
    do
        cmd="./generate.sh -f cssrs01 -e $e -n $n -p $pre"
        echo $cmd
        $cmd
        echo
    done

    cmd="./combine_networks.sh -f cssrs01 -e $e"
    echo $cmd
    $cmd
    echo

done

echo Now submit data as:
echo ./submit.sh -f cssrs01 -e baseline -u tbillah
echo ./submit.sh -f cssrs01 -e month_2 -u tbillah

