#!/usr/bin/env python

import sys
import pandas as pd
from subprocess import check_call
from datetime import datetime, timedelta

data_file=sys.argv[1]

with open(data_file) as f:
    content=f.read().strip().split('\n')


f=open(data_file.replace('.txt','.csv'),'w')
f.write('subjectkey,src_subject_id,interview_date,interview_age,sex,visit,experiment_id,data_file1,data_file1_type\n')

visit='baseline' if 'baseline' in visit else 'month_2'

for line in content:
    # /data/predict1/data_from_nda/Pronet/PHOENIX/GENERAL/PronetBI/processed/BI12345/eeg/ses-20230420/BI12345_eeg_visit001.zip
    elements=line.split('/')
    src_subject_id=elements[9]
    ses=elements[11]
    date=ses.split('ses-')[-1]

    
    interview_date=datetime.strptime(date,'%Y%m%d').strftime('%m/%d/%Y')

    f.write(f',{src_subject_id},{interview_date},,,{visit},2201,{line},BrainVision Core Data Format 1.0\n')


f.close()

