#!/usr/bin/env python

import pandas as pd
import sys
from os.path import abspath, dirname

sys.path.append(dirname(abspath(__file__)))

from idvalidator import validate

# TBD revision: accept input dir and execute for both p1p8 and p9ac32

dfpsychs=pd.read_csv(sys.argv[1])
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
# TBD add _fu_hc.csv suffixes in EntryStatus form or try/except logic in rpms_to_redcap.py

dfhc.reset_index(inplace=True)
outfile=sys.argv[1].replace('_fu_','_fu_hc_')
dfhc.to_csv(outfile,index=False)


