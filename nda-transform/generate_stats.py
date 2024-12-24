#!/usr/bin/env python

from glob import glob
from json import load
import pandas as pd
from os.path import basename, dirname, abspath, join as pjoin

# cd /data/predict1/to_nda/nda-submissions/network_combined

count={}
for e in 'ProNET PRESCIENT CHR HC'.split():
    count[e]=0

files=sorted(glob('*csv'))
# if len(files)<30:
#     print('Execute it within network_combined folder')
#     exit(1)

common=pd.read_csv('ndar_subject01.csv', header=1, dtype=str).set_index('src_subject_id')

with open('/data/predict1/utility/subject-id-gen/sites.json') as f:
    sites=load(f)

stat=pd.DataFrame(columns='File ProNET PRESCIENT CHR HC'.split())
for i,file in enumerate(files):

    print('Processing', file)

    df=pd.read_csv(file, header=1, dtype=str)

    for j,row in df.iterrows():
        s=row['src_subject_id']

        for obj in sites:
            if obj['id']==s[:2]:
                count[obj['network']]+=1
                break

        count[common.loc[s,'phenotype']]+=1


    stat.loc[i]=[file]+list(count.values())

stat.to_csv('stats_by_file.txt',index=False)

