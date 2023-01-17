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

    dfpsychs=pd.read_csv(file)
    dfhc=pd.DataFrame(columns=[c.replace('chrpsychs','hcpsychs') for c in dfpsychs.columns])

    dfpsychs.set_index('subjectkey',inplace=True)
    dfhc.set_index('subjectkey',inplace=True)

    dfincl=pd.read_csv(sys.argv[2])

    j=0
    for i,row in dfincl.iterrows():
        
        if not validate(row['subjectkey']):
            continue
           
        if row['chrcrit_part']==1:
            # CHR
            continue
        
        try:
            dfhc.loc[row['subjectkey']]=dfpsychs.loc[row['subjectkey']].values
        except KeyError:
            continue
        
        j+=1
      
    # TBD dtype conversion

    dfhc.reset_index(inplace=True)
    outfile=sys.argv[1].replace('_fu_','_fu_hc_')
    dfhc.to_csv(outfile,index=False)


chdir(dir_bak)

