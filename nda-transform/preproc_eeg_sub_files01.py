#!/usr/bin/env python

import sys
import pandas as pd
from datetime import datetime, timedelta
import re

with open(sys.argv[1]) as f:
    rows=f.read().strip().split()


f=open(sys.argv[1].replace('.txt','.csv'),'w')
f.write('subjectkey,src_subject_id,interview_date,interview_age,sex,experiment_id,data_file1,data_file1_type\n')


df1=pd.read_csv(f'/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/date_offset.csv')
df2=pd.read_csv(f'/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/date_offset.csv')
date_offset=pd.concat([df1,df2])


date_offset.set_index('subject',inplace=True)
_format='%Y-%m-%d'

for r in rows:
    
    sub=re.search('processed/(.+?)/eeg',r).group(1)
    date=re.search('ses-(.+?)/',r).group(1)
    # 20230125, 20221231, etc.
    # transform it to REDCap date YYYY-MM-DD

    value=f'{date[:4]}-{date[4:6]}-{date[6:]}'
    shift=date_offset.loc[sub,'days']
    value=datetime.strptime(value,_format)+timedelta(days=int(shift))
    shifted_date=value.strftime(_format)

    f.write(f',{sub},{shifted_date},,,2201,{r},zip\n')

f.close()

