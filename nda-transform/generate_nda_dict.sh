#!/bin/bash

TO_NDA=/data/predict1/to_nda
cd ${TO_NDA}/nda-submissions/network_combined

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

"""
import pandas as pd
from glob import glob
import sys

files=glob('*_definitions.csv')

# load list of variables
with open(sys.argv[1]) as f:
    vars=f.read().strip().split()


# create list of definitions
dfall={}
for file in files:
    df=pd.read_csv(file,header=1)
    name=file.split('_definitions.csv')[0]
    dfall[name]=df
    

# now search for variables
for v in vars:
    for df in dfall:

        found=0
        for i,row in df.iterrows():
            if row['Variable Name']==v:
                # write it out
                found=1
                break
            
            elif v in ['Aliases']:
                # write it out
                found=1
                break
        
        if found:
            break

""" > /tmp/generate_nda_dict.py

cd ${TO_NDA}/nda-templates/
python /tmp/generate_nda_dict.py $OUT


: << COMMENT

DICT=${OUT//txt/csv}
rm $DICT
for v in $(cat $OUT)
do
    echo $v
    grep -h -w "\"${v}\"," *_definitions.csv >> $DICT
    grep -h -w "${v}," *_definitions.csv >> $DICT
done

COMMENT

