#!/usr/bin/env python

import pandas as pd
import sys
from os.path import abspath, isfile
import numpy as np

COMBINED_STUDY='combined'

COMBINED_SUBJECT=sys.argv[1]
metadata= sys.argv[2]
files= sorted(sys.argv[3:])


if isinstance(files, list):
    suffix= files[0][11:]
else:
    print('No subject level files are present')
    exit(0)


# read subject-level summary
# generate combined list of datatype
columns=[]
for f in files:
    for c in pd.read_csv(f).columns:
        if c not in columns:
            columns.append(c)

dfnew= pd.DataFrame(columns=columns)

print('\n\nGenerating network level summary\n')

cases=[]
for i,f in enumerate(files):

    print(f)

    df= pd.read_csv(f)
    # subjects for which a datatype is nonexistent
    # will get NaN values under datatype column
    # the NaN values convert the whole column to float
    dfnew.loc[i]=df.loc[0]


# deal with the NaN values in three steps

# 1. remove the NaN values
dfnew.fillna(-9999, inplace=True)

# 2. restore the integers
dtype= {}
for d in dfnew.columns.values[6:]:
    if d in ['reftime', 'timeofday', 'weekday', 'mtime'] or \
        d.endswith('_date') or d.endswith('_missing'):
        continue
    dtype[d]= 'short'
    
dfnew= dfnew.astype(dtype)

# 3. reset the mandatory columns
dfnew[['reftime', 'timeofday', 'weekday']]=''
# Justin Baker and Habib Rahimi asked for removal of all 0s
dfnew.replace(-9999,'',inplace=True)

# sort dfnew by mtime
if 'mtime' in dfnew.columns:
    dfnew.sort_values(by='mtime', ascending=False, inplace=True)

# populate day column
dfnetw= dfnew.copy()
dfnetw['day']= [i+1 for i in range(dfnew.shape[0])]

outfile= f'{COMBINED_STUDY}-{COMBINED_SUBJECT}-{suffix}'
dfnetw.to_csv(outfile, index=False)


print('\n\nGenerating site level summary\n')

if isfile(metadata):
    dfmeta= pd.read_csv(metadata)
else:
    dfmeta= pd.DataFrame(columns=['Subject ID','Active','Consent','Study'])

sites=dfmeta['Subject ID'].values
write=0

i= dfmeta.shape[0]
for site,dfsite in dfnew.groupby('site'):
    
    dfsite.reset_index(inplace=True, drop=True)

    dfsitemeta= pd.DataFrame(columns=['Subject ID','Active','Consent','Study'])
    # reset day column
    for d in range(dfsite.shape[0]):
        dfsite.at[d,'day']= d+1
        dfsitemeta.loc[d]= [dfsite.loc[d,'subject_id'],1,'-',site]

    dfsitemeta.to_csv(f'{site}_metadata.csv', index=False)
    
    outfile= f'{COMBINED_STUDY}-{site}-{suffix}'
    dfsite.to_csv(outfile, index=False)

    # generate metadata
    if site not in sites:
        dfmeta.loc[i]=[site,1,'-',COMBINED_STUDY]
        i+=1
        write=1



# append combined row
if COMBINED_SUBJECT not in sites:
    dfmeta.loc[i]=[COMBINED_SUBJECT,1,'-',COMBINED_STUDY]

if write:
    dfmeta.to_csv(metadata, index=False)

