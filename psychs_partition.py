#!/usr/bin/env python

import pandas as pd
import sys
from os.path import abspath, dirname
from os import getcwd, chdir
from glob import glob

sys.path.append(dirname(abspath(__file__)))

from idvalidator import validate


dir_bak=getcwd()
chdir(sys.argv[1])

files=[glob(p)[0] for p in ['PrescientStudy_Prescient_psychs_p1p8_fu_*.csv','PrescientStudy_Prescient_psychs_p9ac32_fu_*.csv']]

for file in files:
    print(file)

    dfpsychs=pd.read_csv(file)
    dfchr=pd.DataFrame(columns=dfpsychs.columns)
    dfhc=pd.DataFrame(columns=[c.replace('chrpsychs','hcpsychs') for c in dfpsychs.columns])

    dfpsychs.set_index('subjectkey',inplace=True)
    dfchr.set_index('subjectkey',inplace=True)
    dfhc.set_index('subjectkey',inplace=True)

    dfincl=pd.read_csv(sys.argv[2])

    for i,row in dfincl.iterrows():
        
        if not validate(row['subjectkey']):
            continue
           
        if row['chrcrit_part']==1:
            # CHR
            outfile=file
            frame=dfchr
        elif row['chrcrit_part']==2:
            # HC
            outfile=file.replace('_fu_','_fu_hc_')
            frame=dfhc
        else:
            # irrelevant
            continue
            
        try:
            subject_row=dfpsychs.loc[row['subjectkey']].values
            if subject_row.shape[0]<10:
                # this subject has multiple rows, could be a test subject
                # 10 is a safe threshold as single row length > 500
                continue
                # in future, we can just extract the last (presumably latest) row

            frame.loc[row['subjectkey']]=subject_row
        except KeyError:
            continue
        
        print(row['subjectkey'])
        
    # TBD dtype conversion

    frame.reset_index(inplace=True)
    frame.to_csv(outfile,index=False)


chdir(dir_bak)

