#!/usr/bin/env python

import pandas as pd
import sys
from os.path import abspath, isfile
import numpy as np

COMBINED_STUDY='files'

COMBINED_SUBJECT=sys.argv[1]
metadata= sys.argv[2]
files= sorted(sys.argv[3:])

if sys.argv[3]=='*-flowcheck-day1to1.csv':
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
dfnew.fillna(0, inplace=True)

# 2. restore the integers
dtype= {}
for d in dfnew.columns.values[7:]:
    dtype[d]= 'short'
dfnew= dfnew.astype(dtype)

# 3. reset the mandatory columns
# dfnew[['reftime', 'timeofday', 'weekday']]=''
# Justin Baker and Habib Rahimi asked for removal of all 0s
dfnew.replace(0,'',inplace=True)

# sort dfnew by mtime
dfnew.sort_values(by='mtime', ascending=False, inplace=True)

# populate day column
dfnetw= dfnew.copy()
dfnetw['day']= [i+1 for i in range(dfnew.shape[0])]

outfile= f'{COMBINED_STUDY}-{COMBINED_SUBJECT}-flowcheck-day1to9999.csv'
dfnetw.to_csv(outfile, index=False)


print('\n\nGenerating site level summary\n')

if isfile(metadata):
    dfmeta= pd.read_csv(metadata)
else:
    dfmeta= pd.DataFrame(columns=['Subject ID','Active','Consent','Study'])


i= dfmeta.shape[0]
for site,dfsite in dfnew.groupby('site'):
    
    dfsite.reset_index(inplace=True, drop=True)

    dfsitemeta= pd.DataFrame(columns=['Subject ID','Active','Consent','Study'])
    # reset day column
    for d in range(dfsite.shape[0]):
        dfsite.at[d,'day']= d+1
        dfsitemeta.loc[d]= [dfsite.loc[d,'subject_id'],1,'-',site]

    dfsitemeta.to_csv(f'{site}_metadata.csv', index=False)
    
    outfile= f'{COMBINED_STUDY}-{site}-flowcheck-day1to9999.csv'
    dfsite.to_csv(outfile, index=False)

    # generate metadata
    dfmeta.loc[i]=[site,1,'-',COMBINED_STUDY]
    i+=1



# append combined row
dfmeta.loc[i]=[COMBINED_SUBJECT,1,'-',COMBINED_STUDY]

dfmeta.to_csv(metadata, index=False)

