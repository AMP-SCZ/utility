#!/usr/bin/env python

import pandas as pd
import sys


if sys.argv[1] in ['-h', '--help'] or len(sys.argv)<3:
    print(f'Usage: {__file__} /path/to/nda_file01.csv validation_results_*csv')
    exit()


df=pd.read_csv(sys.argv[1],header=1,dtype=str)
dferror=pd.read_csv(sys.argv[2])

dferror1=dferror.copy()
dferror1['src_subject_id']=''
dferror1['VALUE']=''

# RECORD is 1-indexed
# df is 0-indexed
# RECORD=i matches with df.loc[i-1]
for i,row in dferror.iterrows():
    ind=row['RECORD']-1
    dferror1.loc[i,'src_subject_id']= df.loc[ind,'src_subject_id']
    dferror1.loc[i,'VALUE']= df.loc[ind,row['COLUMN']]

dferror1.drop('FILE ID STATUS EXPIRATION_DATE'.split(),axis=1,inplace=True)
dferror1.to_csv(sys.argv[2]+'.augmented',index=False)

