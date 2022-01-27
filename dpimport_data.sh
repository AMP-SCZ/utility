#!/usr/bin/env bash

cd /data/predict/kcho/flow_test/

source /opt/dpdash/miniconda3/bin/activate && \
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/files-*-flowcheck-day1to9999.csv" && \
import.py -c /opt/dpdash/dpimport/examples/config.yml files_metadata.csv
