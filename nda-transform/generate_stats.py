#!/usr/bin/env python

from glob import glob
from json import load
import pandas as pd
from os import getcwd
import sys

if 'network_combined' not in getcwd() or (len(sys.argv)>1 and sys.argv[1]=='-h'):
    print(f'''Usage:
{__file__}
Execute it within network_combined folder''')
    exit(1)


files=['ndar_subject01.csv']
_files=sorted(glob('*csv'))
_files.remove('ndar_subject01.csv')
files+=[x for x in _files]

common=pd.read_csv('ndar_subject01.csv', header=1, dtype=str).set_index('src_subject_id')

with open('/data/predict1/utility/subject-id-gen/sites.json') as f:
    sites=load(f)

stat=pd.DataFrame(columns='File ProNET PRESCIENT CHR HC'.split())
for i,file in enumerate(files):

    print('Processing', file)

    df=pd.read_csv(file, header=1, dtype=str)
    groups=df.groupby('src_subject_id')

    count={}
    for e in 'ProNET PRESCIENT CHR HC'.split():
        count[e]=0


    for s in groups.groups.keys():

        for obj in sites:
            if obj['id']==s[:2]:
                count[obj['network']]+=1
                break

        count[common.loc[s,'phenotype']]+=1


    stat.loc[i]=[file.replace('.csv','')]+list(count.values())


pd.set_option("display.max_rows", None)
print(stat)

stat.to_csv('stats_by_file.txt',index=False)

