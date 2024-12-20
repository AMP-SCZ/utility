#!/usr/bin/env python

import pandas as pd
import sys

pro=pd.read_csv('/data/predict1/data_from_nda/Pronet/PHOENIX/PROTECTED/date_offset.csv')
pre=pd.read_csv('/data/predict1/data_from_nda/Prescient/PHOENIX/PROTECTED/date_offset.csv')
dfshift=pd.concat((pro,pre)).set_index('subject')

df=pd.read_csv(sys.argv[1])
df1=df.copy()

df1.drop(['day','redcap_event_name'],axis=1,inplace=True)
df1['visit']= list(map(lambda x: x.split('_arm_')[0],df['redcap_event_name']))

t=[None]*df.shape[0]
for i,row in df.iterrows():
    t[i]='{}/interviews/{}/{}'.format(row['src_subject_id'],row['interview_type'],row['transcript_file'])

df1['transcript_file']=t
df1['subjectkey']=''
df1['sex']=''

df1.to_csv(sys.argv[1].replace('.csv','_nda.csv'),index=False)

