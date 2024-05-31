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
    
    with open(file) as f:
        _name=f.read().split('\n')[0]
        _name=_name.replace('\"','')
        _name=_name.replace(',','')
    
    for c in df.columns:
        
        if c in 'subjectkey src_subject_id sex interview_date interview_age ampscz_missing ampscz_missing_spec':
            continue
    
        if c not in vars:
            vars[_name+'&'+c]=''
        
print('Total variables found:', len(vars))

# grep pattern formation work
with open(sys.argv[1],'w') as f:
    for v in vars:
        f.write(v+'\n')

""" > /tmp/generate_nda_list.py

OUT=${TO_NDA}/nda_vars.txt
python /tmp/generate_nda_list.py $OUT

echo
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
for _v in tqdm(vars):
    name,v=_v.split('&')
    
    found=0
    for i,row in dfall[name].iterrows():
        if row['ElementName']==v:
            # write row out
            found=1
            break
    
        elif not pd.isna(row['Aliases']) and v in row['Aliases']:
            # write row out
            found=1
            break
    
    if found:
        # remove unwarranted line breaks
        d=row['ElementDescription']
        if not pd.isna(d) and '\n' in d:
            row['ElementDescription']=d.replace('\n',' ')

        # have uploaded variable names in the first column
        row['ElementName']=v
        row['nda_short_name']=name

        rows.append(row)
    else:
        print('Not found:',v)

dfdict=pd.DataFrame(rows,columns=['nda_short_name']+list(df.columns))
dfdict.to_csv(sys.argv[1].replace('.txt','.csv'),index=False)

print('Total variables in dictionary:',dfdict.shape[0])

""" > /tmp/generate_nda_dict.py

cd ${TO_NDA}/nda-templates/
python /tmp/generate_nda_dict.py $OUT


