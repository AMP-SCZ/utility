#!/bin/bash

cd /data/predict1/to_nda/nda-submissions/network_combined


rm ndar_subject01_rejected.txt
cat ../ndar_subject01_Pronet_rejected.txt > ndar_subject01_rejected.txt
tail -n+2 ../ndar_subject01_Prescient_rejected.txt >> ndar_subject01_rejected.txt

