#!/bin/bash

NDA_ROOT=$1

/data/predict1/miniconda3/bin/python /data/predict1/eeg-qc-dash/insert_auto_scores.py
rsync -av $NDA_ROOT/.scores.pkl rc-predict-gen.partners.org:$2

