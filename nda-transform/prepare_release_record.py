#!/usr/bin/env python

import pandas as pd
from glob import glob

dfshared=pd.read_csv('ndar_subject01.csv',header=1)
dfshared.set_index('src_subject_id',inplace=True)

# columns=glob('*csv')
columns=['actirec01.csv', 'ampscz_dim01.csv', 'ampscz_hcgfb01_screening.csv', 'ampscz_iqa01_baseline.csv', 'ampscz_lapes01_screening.csv', 'ampscz_nsipr01_baseline.csv', 'ampscz_psychs01_baseline.csv', 'ampscz_psychs01_screening.csv', 'ampscz_rap01_baseline.csv', 'ampscz_rs01.csv', 'ampscz_sp_sensors01_3705.csv', 'ampscz_sp_sensors01_4366.csv', 'ampscz_sp_survey01.csv', 'assist01_baseline.csv', 'bprs01_baseline.csv', 'cgis01_baseline.csv', 'clgry01_baseline.csv', 'cssrs01_baseline.csv', 'dsm_iv_es01_baseline.csv', 'dsm_iv_es01_screening.csv', 'eeg_sub_files01_baseline.csv', 'figs01.csv', 'gfs01_chrgfrs.csv', 'gfs01_chrgfss.csv', 'iec01.csv', 'image03_baseline.csv', 'langsamp01_baseline_open.csv', 'ndar_subject01.csv', 'oasis01_baseline.csv', 'pds01.csv', 'pmod01_baseline.csv', 'pss01_baseline.csv', 'scidvapd01_screening.csv', 'socdem01.csv', 'sri01_baseline.csv', 'tbi01_screening.csv', 'wais_iv_part101_baseline.csv', 'wasi201_baseline.csv', 'wisc_v01_baseline.csv']

dfupload=pd.DataFrame(columns=['src_subject_id']+columns)
dfupload['src_subject_id']=dfshared.index
dfupload.set_index('src_subject_id',inplace=True)

for file in columns:
    
    count=0
    dfdata=pd.read_csv(file,header=1)
    dfdata.set_index('src_subject_id',inplace=True)
    
    for s in dfshared.index:
        try:
            dfdata.loc[s]
            dfupload.at[s,file]='\u2713'
            count+=1
        except:
            pass
    
    print(f'{file:30}',count)

dfupload.to_csv('ampscz-release-1.0-record.csv')

