#!/bin/bash

NDA_ROOT=$1
cd $NDA_ROOT
rsync -avR */PHOENIX/PROTECTED/*/processed/*/eeg/*/Figures/*[!QC].png \
-avR */PHOENIX/PROTECTED/*/processed/*/eeg/*/Figures/WU01590_20220921_runSheet.* \
rc-predict-gen.partners.org:/data/EEGqc/

