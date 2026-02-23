#!/usr/bin/env python

import pandas as pd
import json
import sys
from shutil import copyfile
from os.path import basename

if len(sys.argv)<3 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
{__file__} /path/to/figs/redcap/export.csv /data/predict1/utility/yale-real/orig/pronet_dict_20250224.csv''')
    exit()

# load FIGS REDCap's CSV export
df= pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)

# load data dictionary
ddict= pd.read_csv(sys.argv[2], dtype=str)

# find FIGS calc variables
vars=[]
for i,row in ddict.iterrows():
    if row['form_name']=='family_interview_for_genetic_studies_figs':
        if row['field_type']=='calc':
            v= row['field_name']
            if v in df.columns:
                vars.append(row['field_name'])
            else:
                pass
                # print(v)



def REPLACE():
    for i,row in df.iterrows():
        s= row['study_id']
        site= s[:2]

        file= f'/data/predict1/data_from_nda/Prescient/PHOENIX/GENERAL/Prescient{site}/processed/{s}/surveys/{s}.Prescient.json'

        # print('Processing', file)

        # load json
        with open(file) as f:
            dict1=json.load(f)


        # replace FIGS calc fields
        REWRITE=False
        for d in dict1:
            if d['redcap_event_name']==row['redcap_event_name']:
                for v in vars:
                    if d[v] != row[v]:
                        REWRITE=True
                        d[v]= row[v]

            break

        copyfile(file, file+'.bak')

        if REWRITE:
            print(file)
            with open(file,'w') as f:
                json.dump(dict1,f)


def VERIFY():
    for i,row in df.iterrows():
        s= row['study_id']
        site= s[:2]

        file= f'/data/predict1/data_from_nda/Prescient/PHOENIX/GENERAL/Prescient{site}/processed/{s}/surveys/{s}.Prescient.json'

        # print('Verifying', file)

        # load json
        with open(file) as f:
            dict1=json.load(f)


        # replace FIGS calc fields
        REWRITE=False
        for d in dict1:
            if d['redcap_event_name']==row['redcap_event_name']:
                for v in vars:
                    if d[v] != row[v]:
                        print(f'{basename(file)},{v},{d[v]},{row[v]}')

            break


REPLACE()
# VERIFY()
