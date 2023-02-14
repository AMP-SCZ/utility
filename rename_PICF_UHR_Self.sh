#!/bin/bash

cd /mnt/prescient/RPMS_incoming/

sed -i "s/PICF_UHR_Self_V3/PICF_UHR_Self_V2/g" PrescientStudy_Prescient_entry_status_*csv
sed -i "s/PICF_UHR_Self_V4/PICF_UHR_Self_V2/g" PrescientStudy_Prescient_entry_status_*csv

