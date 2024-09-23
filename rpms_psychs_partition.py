#!/usr/bin/env python

import pandas as pd
import sys
from datetime import date, datetime
from os.path import abspath, dirname
from os import getcwd, chdir
from glob import glob

sys.path.append(dirname(abspath(__file__)))

from idvalidator import validate

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
./{__file__} /path/to/RPMS_incoming/
./{__file__} /path/to/RPMS_incoming/ 31.12.2022.csv
Splits PSYCHS follow up forms into CHRs and HCs''')
    exit(0)

try:
    suffix=sys.argv[2]
except:
    suffix=date.today().strftime('%d.%m.%Y.csv')

dir_bak=getcwd()
chdir(sys.argv[1])

files=[glob(p)[0] for p in [f'PrescientStudy_Prescient_psychs_p1p8_fu_{suffix}',
    f'PrescientStudy_Prescient_psychs_p9ac32_fu_{suffix}']]

for file in files:
    print(file)

    dfpsychs=pd.read_csv(file,dtype=str)
    dfchr=pd.DataFrame(columns=dfpsychs.columns)
    dfhc=pd.DataFrame(columns=[c.replace('chrpsychs','hcpsychs') for c in dfpsychs.columns])

    dfpsychs.set_index('subjectkey',inplace=True)
    dfchr.set_index('subjectkey',inplace=True)
    dfhc.set_index('subjectkey',inplace=True)

    dfincl=pd.read_csv(glob('PrescientStudy_Prescient_inclusionexclusion_criteria_review_*.csv')[0])
    dfconsent=pd.read_csv(glob('PrescientStudy_Prescient_informed_consent_run_sheet_*.csv')[0])
    dfconsent.set_index('subjectkey',inplace=True)

    for i,row in dfincl.iterrows():
        
        if not validate(row['subjectkey']):
            continue
           
        try:
            # additional [ ] used around row['subjectkey']
            # to make the result a row when there is a single row
            subject_row=dfpsychs.loc[ [row['subjectkey']] ]
        except KeyError:
            continue
        
        s=row['subjectkey']

        try:
            chr_hc= int(row['chrcrit_part'])
            if chr_hc==1:
                chr_hc='UHR'
            elif chr_hc==2:
                chr_hc='HealthyControl'

        except ValueError:
            # chrcrit_part is empty for this subject
            print(s)
            print('\tattempt to infer chrcrit_part from group column in informed_consent_run_sheet')

            # extract Young Patient's rows only, we do not need Guardian's rows
            # to account for re-consent scenario, consider only the last row
            try:
                group1= dfconsent.loc[[row['subjectkey']]]
            except KeyError:
                print('\tdoes not seem to have been consented\n')
                continue
            
            yp= group1[group1['version']=='YP']
            yp_sorted= yp.sort_values('interview_date',
                key=lambda dates: [datetime.strptime(x,'%m/%d/%Y') for x in dates])
            chr_hc= yp_sorted.iloc[-1]['group']


        if chr_hc=='UHR':
            # CHR
            dfchr=pd.concat([dfchr,subject_row])
        elif chr_hc=='HealthyControl':
            # HC
            subject_row.columns=dfhc.columns
            dfhc=pd.concat([dfhc,subject_row])
        else:
            # irrelevant
            print(f'CHR/HC status could not be determined')
            continue

    print('')
        

    outfile=file
    dfchr=dfchr.reset_index()
    dfchr.to_csv(outfile,index=False)

    outfile=file.replace('_fu_','_fu_hc_')
    dfhc=dfhc.reset_index()
    dfhc.to_csv(outfile,index=False)


chdir(dir_bak)

