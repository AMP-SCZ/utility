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
        
        if c in 'subjectkey src_subject_id sex interview_date interview_age':
            continue
    
        if c not in vars:
            vars[c]=''
        
print('Total variables found:', len(vars))

# grep pattern formation work
with open(sys.argv[1],'w') as f:
    for v in vars:
        f.write(v+'\n')

""" > /tmp/generate_nda_dict.py


OUT=${TO_NDA}/nda_vars.txt
python /tmp/generate_nda_dict.py $OUT


cd ${TO_NDA}/nda-templates/
DICT=${OUT//txt/csv}
rm $DICT
for v in $(cat $OUT)
do
    grep -h $v *_definitions.csv >> $DICT
done

