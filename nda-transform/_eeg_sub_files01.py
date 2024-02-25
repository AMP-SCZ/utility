#!/usr/bin/env python

import sys

data_file=sys.argv[1]

with open(data_file) as f:
    content=f.read().strip().split('\n')

f=open(data_file.replace('.txt','.csv'),'w')
f.write('subjectkey,src_subject_id,interview_date,interview_age,sex,experiment_id,data_file1,data_file1_type\n')

for line in content:
    # /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetBI/processed/BI05652/eeg/ses-20230420/NDA/BI05652_eeg_visit001.zip
    elements=line.split('/')
    src_subject_id=elements[9]
    _date=elements[11].split('ses-')[-1]
    interview_date=f'{_date[:4]}-{_date[4:6]}-{_date[6:8]}'
    
    f.write(f',{src_subject_id},{interview_date},,,,2201,{line},\n')

f.close()

