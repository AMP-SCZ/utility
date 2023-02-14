#!/bin/bash

cd /mnt/prescient/RPMS_incoming/

sed -i "s/PICF_UHR_Self_V2,100/PICF_UHR_Self_V2,1/g" PrescientStudy_Prescient_entry_status_*csv
sed -i "s/PICF_UHR_Self_V3,100/PICF_UHR_Self_V2,1/g" PrescientStudy_Prescient_entry_status_*csv
# sed -i "s/PICF_UHR_Self_V4,100/PICF_UHR_Self_V2,1/g" PrescientStudy_Prescient_entry_status_*csv

