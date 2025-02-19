#!/bin/bash

export PATH=/data/predict1/miniconda3/bin/:$PATH

cd /data/predict1/to_nda/nda-submissions/network_combined

vtcmd -d ampscz-release-3.0 -t ampscz-release-3.0 -c 3705 -u tbillah -f *csv -b -l .

