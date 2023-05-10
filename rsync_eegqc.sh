#!/bin/bash

NDA_ROOT=$1
cd $NDA_ROOT

for d in `ls -d */PHOENIX/PROTECTED/*/`
do
    rsync -avR ${d}/processed/*/eeg/*/Figures/*[!QC].png rc-predict-gen.partners.org:$2
    rsync -avR ${d}/processed/*/eeg/*/Figures/*_runSheet.* rc-predict-gen.partners.org:$2
done


