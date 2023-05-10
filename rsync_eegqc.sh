#!/bin/bash

NDA_ROOT=$1
cd $NDA_ROOT

for d in `ls -d */PHOENIX/PROTECTED/*/processed/*/eeg/*/Figures`
do
    rsync -avR ${d}/*[!QC].png rc-predict-gen.partners.org:$2
    rsync -avR ${d}/*_runSheet.* rc-predict-gen.partners.org:$2
done
