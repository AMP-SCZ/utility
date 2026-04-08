#!/usr/bin/env python

import pandas as pd
from shutil import move
from tempfile import mkstemp
import sys
from os import remove

def detect_anomaly(df1):
    df2=df1.copy()

    # check only variables of String type
    str_columns=[]    
    for c in df1.columns:
        try:
            if dict1.loc[c,'DataType']=='String':
                str_columns.append(c)
        except KeyError:
            pass

    REWRITE=False
    for i,row in df1.iterrows():
        for c in str_columns:

            value=row[c]
            if pd.isna(value):
                continue

            if '\"' in value:
                REWRITE=True
                print(i,c,'\n',value)
                value=value.replace('\"','')
                df2.loc[i,c]=value

            if '\n' in value:
                REWRITE=True
                print(i,c,'\n',value)
                value=value.replace('\n',' ')
                df2.loc[i,c]=value

    if REWRITE:
        return df2
    else:
        return None


df= pd.read_csv(sys.argv[1],header=1,dtype=str)

dict1= pd.read_csv('/data/predict1/to_nda/nda-templates/'+sys.argv[2]+'_definitions.csv')
dict1.set_index('ElementName',inplace=True)


print('Detect and cure anomalies in', sys.argv[1])
df1= detect_anomaly(df)

if df1 is None:
    exit()
else:
    print('Recheck anomalies')
    BAD= detect_anomaly(df1)
    if not BAD:
        # rewrite file

        # get title
        with open(sys.argv[1]) as f:
            title= f.read().split('\n')[0]

        # backup original
        move(sys.argv[1],'/data/predict1/to_nda/nda-submissions/network_combined/original/'+sys.argv[1]+'.problem')

        # append title
        _,name=mkstemp()
        df1.to_csv(name,index=False)
        
        with open(name) as f:
            data=f.read()
        remove(name)

        with open(sys.argv[1],'w') as f:
            f.write(title+'\n'+data)


