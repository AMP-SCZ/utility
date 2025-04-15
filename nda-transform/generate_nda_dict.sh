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
        
        if c in 'subjectkey src_subject_id sex interview_date interview_age visit ampscz_missing ampscz_missing_spec':
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


# these variables are common across all data structures
: << COMMENT
COMMON,"ElementName","DataType","Size","Required","ElementDescription","ValueRange","Notes","Aliases"
COMMON,"subjectkey","GUID","","Required","The NDAR Global Unique Identifier (GUID) for research subject","NDAR*","",""
COMMON,"src_subject_id","String","20","Required","Subject ID how it's defined in lab/project","","",""
COMMON,"interview_date","Date","","Required","Date on which the interview/genetic test/sampling/imaging/biospecimen was completed. MM/DD/YYYY","","",""
COMMON,"interview_age","Integer","","Required","Age in months at the time of the interview/test/sampling/imaging.","0::1440","Age is rounded to chronological month. If the research participant is 15-days-old at time of interview, the appropriate value would be 0 months. If the participant is 16-days-old, the value would be 1 month.",""
COMMON,"sex","String","20","Required","Sex of subject at birth","M;F; O; NR","M = Male; F = Female; O=Other; NR = Not reported",""
COMMON,"visit","String","60","Recommended","Visit name","","",""
COMMON,"ampscz_missing","Integer","","Recommended","Please click if this form is missing all of its data","0;1","0 = Not clicked; 1 = Clicked",
COMMON,"ampscz_missing_spec","Integer","","Recommended","Please specify the reason for missing data on this form","0::6","0 = Evaluation not necessary because the screening visit was less than 21 days from baseline visit; 1 = Measure refusal (no reason provided); 2 = No show; 3 = Research assistant forgot; 4 = Uncontrollable circumstance; 5 = Participant dropped out; 6 = Evaluation not necessary because the screening visit was less than 21 days from baseline visit",
COMMENT


