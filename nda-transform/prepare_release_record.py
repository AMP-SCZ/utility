#!/usr/bin/env python

import pandas as pd
from glob import glob
import sys
from os.path import isfile
from os import remove

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
Execute this script within to_nda/nda-submissions/network_combined/ directory:
{__file__} output.csv
Output is ampscz-release-1-record.csv, ampscz-release-2-record.csv, etc.
''')
    exit()

if isfile(sys.argv[1]):
    remove(sys.argv[1])

dfshared=pd.read_csv('ndar_subject01.csv',header=1)
dfshared.set_index('src_subject_id',inplace=True)

columns=sorted(glob('*csv'))

dfupload=pd.DataFrame(columns=['src_subject_id']+columns)
dfupload['src_subject_id']=dfshared.index
dfupload.set_index('src_subject_id',inplace=True)

for file in columns:
    
    count=0
    dfdata=pd.read_csv(file,header=1)
    dfdata.set_index('src_subject_id',inplace=True)
    
    for s in dfshared.index:
        try:
            dfdata.loc[s]
            dfupload.at[s,file]='\u2713'
            count+=1
        except:
            pass
    
    print(f'{file:32}',count)

dfupload.to_csv(sys.argv[1])

