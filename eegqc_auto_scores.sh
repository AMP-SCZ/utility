#!/bin/bash

NDA_ROOT=$1

/data/predict1/miniconda3/bin/python /data/predict1/eeg-qc-dash/insert_auto_scores.py

export LD_LIBRARY_PATH=/apps/software/librsync/2.3.4-GCCcore-13.3.0/lib:$LD_LIBRARY_PATH
export PATH=/apps/software/rsync/3.4.1-GCCcore-13.3.0/bin:$PATH
rsync -av $NDA_ROOT/.scores.pkl $2

