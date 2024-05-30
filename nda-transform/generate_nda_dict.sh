#!/bin/bash

TO_NDA=/data/predict1/to_nda
cd ${TO_NDA}/nda-submissions/network_combined

echo Gathering list of variables uploaded to NDA

echo """
import pandas as pd
from glob import glob
import sys

files=glob('*csv')

vars={}
for file in files:
    df=pd.read_csv(file,header=1)
    
    for c in df.columns:
        
        if c in 'subjectkey src_subject_id sex interview_date interview_age ampscz_missing ampscz_missing_spec':
            continue
    
        if c not in vars:
            vars[c]=''
        
print('Total variables found:', len(vars))

# grep pattern formation work
with open(sys.argv[1],'w') as f:
    for v in vars:
        f.write(v+'\n')

""" > /tmp/generate_nda_list.py

OUT=${TO_NDA}/nda_vars.txt
python /tmp/generate_nda_list.py $OUT


echo Generating combined dictionary of the above list

echo """
import pandas as pd
from glob import glob
import sys
from tqdm import tqdm

files=glob('*_definitions.csv')

# load list of variables
with open(sys.argv[1]) as f:
    vars=f.read().strip().split()


# create list of definitions
dfall={}
for file in files:
    df=pd.read_csv(file)
    name=file.split('_definitions.csv')[0]
    dfall[name]=df
    

# now search for variables
rows=[]
for v in tqdm(vars):
    for name in dfall:

        found=0
        for i,row in dfall[name].iterrows():
            if row['ElementName']==v:
                # write row out
                found=1
                break
            
            elif v in row['Aliases']:
                # write row out
                found=1
                break
        
        if found:
            rows.append(row)
            break

dfdict=pd.DataFrame(rows,columns=df.columns)
dfdict.to_csv(sys.argv[1].replace('.txt','.csv'),index=False)

""" > /tmp/generate_nda_dict.py

cd ${TO_NDA}/nda-templates/
python /tmp/generate_nda_dict.py $OUT


