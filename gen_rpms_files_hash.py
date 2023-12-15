#!/usr/bin/env python

import sys
import hashlib
import pandas as pd
from os.path import abspath, isfile

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {abspath(__file__)} ME57953
execute it within /path/to/ME57953/surveys/ directory
''')
    exit(0)


subject=sys.argv[1]

# read or create hash record
hashfile=f'{subject}_hashes.csv'
if isfile(hashfile):
    df=pd.read_csv(hashfile)
else:
    df=pd.DataFrame(columns='form content_hash upload'.split())

df.set_index('form',inplace=True)



with open('/data/predict1/utility/rpms_file_suffix.txt') as f:
    suffixes=f.read().split()


FORCE=0

# read files, compute and compare hashes
for suffix in suffixes:
    form=f'{subject}_{suffix}'
    
    if isfile(form):
        with open(form) as f:
            content=f.read().strip()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # new file
        try:
            df.loc[form]
        except:
            df.loc[form]=[content_hash,1]
            continue

        # changed determiner
        if df.loc[form,'content_hash']!=content_hash:
            df.loc[form]=[content_hash,1]
            
            # change in these forms may affect CHR/HC designation, so upload all
            if form in [f'{subject}_inclusionexclusion_criteria_review.csv',
                    f'{subject}_informed_consent_run_sheet.csv']:
                FORCE=1

        else:
            df.at[form,'upload']=0


if FORCE:
    df['upload']=[1]*df.shape[0]

df.to_csv(hashfile)


