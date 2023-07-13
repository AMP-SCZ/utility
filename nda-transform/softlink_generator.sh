#!/bin/bash

caselist=/data/predict1/to_nda/nda-submissions/network_combined/all_subjects.txt
rm $caselist


# create caselist

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


# create subject folders

pushd .

cd /data/predict1/to_nda/nda-submissions/network_combined/
for d in $(cat $caselist)
do
    mkdir -p $d
done


# create softlinks to datatypes: eeg, actigraphy, sensors, interviews

for d in $(cat $caselist)
do
    cd $d
    
    # TODO the * can be made definite
    root=`ls -d /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/*/processed/$d`


    # eeg
    ln -s ${root}/eeg .

    # actigraphy
    ln -s ${root}/actigraphy .

    # senors
    ln -s ${root}/phone .

    # interviews
    root=`ls -d /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/*/processed/$d`
    ln -s ${root}/interviews .
    
    cd ..

done


