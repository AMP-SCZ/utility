#!/bin/bash

create_link()
{
    if [ -d $1 ]
    then
        echo $1
        ln -s $1 .
    fi
}


caselist=/data/predict1/to_nda/nda-submissions/network_combined/all_subjects.txt
rm $caselist


echo create caselist

cd /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED

for n in Pronet Prescient
do

    pushd .
    cd /data/predict1/data_from_nda/${n}/PHOENIX/PROTECTED

    for c in `ls -d */raw/*`
    do
        IFS='/' read -ra dirs <<< $c
        echo ${dirs[2]} >> $caselist
    done

    popd
       
done

echo


echo create subject folders

pushd .

cd /data/predict1/to_nda/nda-submissions/network_combined/
for d in $(cat $caselist)
do
    mkdir -p $d
done

echo


echo create softlinks to datatypes: eeg, actigraphy, sensors, interviews

for d in $(cat $caselist)
do
    cd $d
    
    # TODO the * can be made definite
    root=`ls -d /data/predict1/data_from_nda/*/PHOENIX/PROTECTED/*/processed/$d`


    # eeg
    create_link ${root}/eeg .

    # actigraphy
    create_link ${root}/actigraphy .

    # sensors
    create_link ${root}/phone .

    # interviews
    root=`ls -d /data/predict1/data_from_nda/*/PHOENIX/GENERAL/*/processed/$d`
    create_link $root/interviews


    cd ..

done


