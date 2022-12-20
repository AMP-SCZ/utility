#!/usr/bin/env python

from glob import glob
import pandas as pd
from os import getcwd
from os.path import abspath
import sys

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
{__file__} /path/to/combined-SITE-assessment-day1to1.csv "*/processed/*/eeg/??-*-EEGqc-day1to*.csv"
{__file__} /path/to/combined-SITE-assessment-day1to1.csv "./**/??-*-EEGqc-day1to*.csv"

This program combines CSV features at network or site level.
Execute it from any of the example directories:
$NDA_ROOT/Pronet
$NDA_ROOT/Prescient
$NDA_ROOT/Pronet/PHOENIX/PROTECTED/PronetCA
$NDA_ROOT/Prescient/PHOENIX/PROTECTED/PrescientME
with a proper glob() pattern''')
    exit(0)


files= glob(sys.argv[2],recursive=True)
if not files:
    print('No DPdash compatible CSV files to combine, exiting')
    exit()
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


# restore the data types
dtype= {}

# replace the NaNs for the purpose of dtype restoration
# otherwise, we shall get
# pandas.errors.IntCastingNaNError: Cannot convert non-finite values (NA or inf) to integer
# even though we omit 'reftime','timeofday','weekday' from dtype
df1[['reftime', 'timeofday', 'weekday']].fillna(0, inplace=True)
for c,d in zip(df.columns.values,df.dtypes):

    if 'int' in d.name:
        dtype[c]= 'short'
    elif 'float' in d.name:
        dtype[c]= 'float32'
    else:
        dtype[c]= d.name

df1= df1.astype(dtype)

# now reset the mandatory columns
df1[['reftime', 'timeofday', 'weekday']]=''

curr_dir= getcwd()
if curr_dir.endswith('Pronet'):
    site='PRONET'
elif curr_dir.endswith('Prescient'):
    site='PRESCIENT'
else:
    site=curr_dir[-2:]

outfile=sys.argv[1].replace('SITE',site)
print(f'Generating {abspath(outfile)}')

df1.to_csv(outfile, index=False)

