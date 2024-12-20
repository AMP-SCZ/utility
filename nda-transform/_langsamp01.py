#!/usr/bin/env python

import pandas as pd
import sys
from datetime import datetime, timedelta

pro=pd.read_csv('/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/date_offset.csv')
pre=pd.read_csv('/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/date_offset.csv')
dfshift=pd.concat((pro,pre)).set_index('subject')

df=pd.read_csv(sys.argv[1])
df1=df.copy()

df1.drop(['day','redcap_event_name'],axis=1,inplace=True)
df1['visit']= list(map(lambda x: x.split('_arm_')[0],df['redcap_event_name']))


# transcripts are located at:
# {network}/PHOENIX/GENERAL/{site}/processed/{subject}/interviews/{type}/transcripts/*_REDACTED.txt
d=[None]*df.shape[0]
t=[None]*df.shape[0]
for i,row in df.iterrows():
    src_subject_id=row['src_subject_id']
    t[i]='{}/interviews/{}/transcripts/{}'.format(src_subject_id,row['interview_type'],row['transcript_file'])

    shift=int(dfshift.loc[src_subject_id,'days'])
    shifted_date=datetime.strptime(row['interview_date'],'%Y-%m-%d')+timedelta(days=shift)
    d[i]=shifted_date.strftime('%m/%d/%Y')

df1['interview_date']=d
df1['transcript_file']=t
df1['subjectkey']=''
df1['sex']=''

df1.to_csv(sys.argv[1].replace('.csv','_nda.csv'),index=False)

