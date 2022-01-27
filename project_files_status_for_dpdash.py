#!/usr/bin/env python

import pandas as pd
import sys
from os.path import abspath
import numpy as np

COMBINED_STUDY='files'
# COMBINED_SUBJECT='combined'
COMBINED_SUBJECT=sys.argv[1]

files= sorted(sys.argv[2:])

# read Kevin's dataframe
df= pd.read_csv(files[0])

# replace day column, append subject_id column
dfnew= df.copy()

print('\n\nCombining subject level files:\n')

cases=[]
for i,f in enumerate(files):

    print(f)

    # example file name LA-LA00012-flowcheck-day1to1.csv
    cases.append(f.split('-')[1])

    df= pd.read_csv(f)
    dfnew.loc[i]=df.loc[0]

cases=np.unique(cases)
L= len(cases)

# populate subject_id column
dfnew['subject_id']= cases

# sort dfnew by mtime
dfnew.sort_values(by='mtime', ascending=False, inplace=True)

# populate day column
dfnew['day']= [i+1 for i in range(L)]

outfile= f'{COMBINED_STUDY}-{COMBINED_SUBJECT}-flowcheck-day1to9999.csv'
dfnew.to_csv(outfile, index=False)


dfmeta= pd.DataFrame(columns=['Subject ID','Active','Consent','Study'])
# dfmeta['Subject ID']= dfnew['subject_id']
# dfmeta['Active']= [1]*L
# dfmeta['Consent']= ['-']*L
# dfmeta['Study']= [COMBINED_STUDY]*L

# append combined row
dfmeta.loc[0]=[COMBINED_SUBJECT,1,'-',COMBINED_STUDY]

dfmeta.to_csv(f'{COMBINED_STUDY}_metadata.csv', index=False)

