#!/usr/bin/env python

import sys
from os.path import abspath, isfile
from shutil import move
import pandas as pd

if sys.argv[1] in ['-h', '--help'] or len(sys.argv)<3:
    print(f'Usage: ./{__file__} ndar_subject01.csv validation_results_*csv')
    exit()

with open(sys.argv[1]) as f:
    data=f.read().split('\n')

validation=pd.read_csv(sys.argv[2],dtype=str)
error_rows=validation['RECORD'].values
# add 1 to match with 0-indexed data
LE=len(error_rows)
for i in range(LE):
    error_rows[i]=int(error_rows[i])+1

data2=[None]*(len(data)-LE)
j=0
for i,row in enumerate(data):
    if i not in error_rows:
        data2[j]=row
        j+=1

move(sys.argv[1],'/tmp/'+sys.argv[1])
with open(sys.argv[1],'w') as f:
    f.write('\n'.join(data2))

    
