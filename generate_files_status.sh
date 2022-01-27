#!/usr/bin/env bash

export PATH=/data/predict/utility/:$PATH

# use pnlpipe3 environment to bypass the error below
# https://gist.github.com/tashrifbillah/24efeec3219ba3c58c92adc419aac7be#gistcomment-4037001
source /data/pnl/soft/pnlpipe3/miniconda3/bin/activate && conda activate pnlpipe3 && \
subject_files_status_for_dpdash.py && \
cd /data/predict/kcho/flow_test/Pronet_status && \
project_files_status_for_dpdash.py ProNET *-flowcheck-day1to1.csv && \
cd /data/predict/kcho/flow_test/Prescient_status && \
project_files_status_for_dpdash.py PRESCIENT *-flowcheck-day1to1.csv

