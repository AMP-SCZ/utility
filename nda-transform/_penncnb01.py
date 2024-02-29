#!/usr/bin/env python

import pandas as pd
from datetime import datetime
# https://github.com/AMP-SCZ/subject-id-validator/blob/main/idvalidator.py
from idvalidator import validate
import sys


datestamp=datetime.now().strftime('%Y%m%d')
df=pd.read_csv(sys.argv[1],dtype=str)
df1=pd.DataFrame(columns=df.columns)

j=0
for i,row in df.iterrows():
    sub=row['src_subject_id']

    if len(sub)>=7 and len(sub)<=9:
        # all ids like AB12345_1
        _sub=sub[:7]
        if '_' not in _sub and not validate(_sub):
            # all ids like [AB12345]
            _sub=sub[1:8]
            if not validate(_sub):
                continue

        # ab12345-->AB12345
        _sub=_sub.upper()
        
        row['src_subject_id']=_sub
        df1.loc[j]=row
        j+=1


df1.drop(columns=['redcap_id','ndar_penncnb01_complete'],inplace=True)
df1.insert(loc=0,column='subjectkey',value='')
df1.to_csv(sys.argv[1].replace('.csv',f'_{datestamp}.csv'),index=False)

