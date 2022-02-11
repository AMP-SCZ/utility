#!/usr/bin/env bash

cd /data/predict/kcho/flow_test/

source /opt/dpdash/miniconda3/bin/activate && \

# metadata
import.py -c /opt/dpdash/dpimport/examples/config.yml files_metadata.csv && \
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/*_metadata.csv" && \

# project level files status
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/files-*-flowcheck-day1to9999.csv" && \

# subject level files status
import.py -c /opt/dpdash/dpimport/examples/config.yml "*_status/*-flowcheck-day1to1.csv"

