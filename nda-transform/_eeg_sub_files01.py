#!/usr/bin/env python

import sys
import pandas as pd
from subprocess import check_call
from datetime import datetime, timedelta

data_file=sys.argv[1]

with open(data_file) as f:
    content=f.read().strip().split('\n')

pro=pd.read_csv('/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/date_offset.csv')
pre=pd.read_csv('/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/date_offset.csv')
dfshift=pd.concat((pro,pre)).set_index('subject')

f=open(data_file.replace('.txt','.csv'),'w')
f.write('subjectkey,src_subject_id,interview_date,interview_age,sex,experiment_id,data_file1,data_file1_type\n')


for line in content:
    # /data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/PronetBI/processed/BI05652/eeg/ses-20230420/NDA/BI05652_eeg_visit001.zip
    elements=line.split('/')
    src_subject_id=elements[9]
    ses=elements[11]
    date=ses.split('ses-')[-1]

    # shift interview_date
    shift=int(dfshift.loc[src_subject_id,'days'])
    shifted_date=datetime.strptime(date,'%Y%m%d')+timedelta(days=shift)
    interview_date=shifted_date.strftime('%m/%d/%Y')


    # shift ses folder name
    _ses='ses-{}'.format(shifted_date.strftime('%Y%m%d'))
    line=line.replace(ses,_ses)

    # create symlink for shifted ses
    parent=line.split(_ses)[0]
    check_call(f'cd {parent} && if [ ! -d {_ses} ]; then ln -s {ses} {_ses}; fi', shell=True)
    # remove symlink if needed
    # check_call(f'cd {parent} && if [ -d {_ses} ]; then rm {_ses}; fi', shell=True)
    

    f.write(f',{src_subject_id},{interview_date},,,2201,{line},\n')


f.close()

