#!/usr/bin/env python

from glob import glob
import pandas as pd

# cd /data/predict1/to_nda/nda-submissions/network_combined

derived=pd.read_csv('langsamp01_derived.csv',dtype=str,header=1)
files=glob('langsamp01_*_*.csv')


print('check if each derived features row has a row in REDCap features')
surveys={}
for f in files:
    surveys[f]=pd.read_csv(f,dtype=str,header=1).set_index('src_subject_id')


absent=set()
for i,row in derived.iterrows():
    s=row['src_subject_id']
    t=row['interview_type']
    e=row['visit']

    t='open' if t=='1' else 'psychs'

    file=f'langsamp01_{e}_{t}.csv'
    try:
        surveys[file].loc[s]
    except:
        absent.update([f'{s} {file}'])

absent=list(absent)

print(len(absent))
print(absent)




print('check if each REDCap features row has a row in derived features')
ngroups=derived.groupby(['src_subject_id', 'interview_type','visit']).ngroups
derived.set_index(['src_subject_id', 'interview_type','visit'], inplace=True)

# sort_index() to avoid
# PerformanceWarning: indexing past lexsort depth may impact performance.
derived.sort_index(inplace=True)
for i,f in enumerate(files):

    df=pd.read_csv(f,dtype=str,header=1)
    if i==0:
        df1=df.copy()
    else:
        df1=pd.concat((df1,df),ignore_index=True)


absent=[]
for i,row in df1.iterrows():
    s=row['src_subject_id']
    e=row['visit']
    t=row['interview_type']

    try:
        derived.loc[(s,t,e)]
    except:
        absent.append(f" ['{s}','{t}','{e}'] ")

print()
print(len(absent))
print(absent)
print()

# some statistics
print('Total rows in REDCap features:', df1.shape[0])
print('Total unique sessions in derived features:', ngroups)


