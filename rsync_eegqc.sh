#!/bin/bash

NDA_ROOT=$1
cd $NDA_ROOT
rsync -avR */PHOENIX/PROTECTED/*/processed/*/eeg/*/Figures/*[!QC].png \
-avR */PHOENIX/PROTECTED/*/processed/*/eeg/*/Figures/*_runSheet.* \
rc-predict-gen.partners.org:$2

