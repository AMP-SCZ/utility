#!/usr/bin/env python

from glob import glob
import pandas as pd
from os import getcwd
from os.path import abspath
import sys

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {__file__} /path/to/AMPSCZ-SITE-assessment-day1to9999.csv
This program combines CSV features at network or site level.
Execute it from any of the example directories:
$NDA_ROOT/Pronet
$NDA_ROOT/Prescient
$NDA_ROOT/Pronet/PHOENIX/PROTECTED/PronetCA
$NDA_ROOT/Prescient/PHOENIX/PROTECTED/PrescientME''')
    exit(0)


files= glob('./**/*day1to1.csv',recursive=True)
df= pd.read_csv(files[0])

df1= pd.DataFrame(columns= list(df.columns)+['subject'])

i=0
for f in files:
    df= pd.read_csv(f)
    subject= f.split('-')[1]
    
    for _,row in df.iterrows():
        values= list(row)
        df1.loc[i]= list(row)+ [subject]
        df1.at[i,'day']= i+1
        i+=1

curr_dir= getcwd()
if curr_dir.endswith('Pronet'):
    site='ProNET'
elif curr_dir.endswith('Prescient'):
    site='PRESCIENT'
else:
    site=curr_dir[-2:]

outfile=sys.argv[1].replace('SITE',site)
print(f'Generating {abspath(outfile)}')

df1.to_csv(outfile, index=False)

