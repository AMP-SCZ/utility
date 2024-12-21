#!/usr/bin/env python

from glob import glob
import pandas as pd

# cd /data/predict1/to_nda/nda-submissions/network_combined

derived=pd.read_csv('langsamp01_derived.csv',dtype=str,header=1)
files=glob('langsamp01_*_*.csv')

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

