#!/usr/bin/env python

import pandas as pd
from datetime import datetime, timedelta
# https://github.com/AMP-SCZ/subject-id-validator/blob/main/idvalidator.py
from idvalidator import validate
import sys
from os.path import dirname, join as pjoin

datestamp=datetime.now().strftime('%Y%m%d')


if __name__=='__main__':


    if sys.argv[1] in ['-h','--help'] or len(sys.argv)<3:
        print(f'Usage: {__file__} /path/to/penncnb_*.csv replace')
        print(f'Usage: {__file__} /path/to/penncnb_*.csv shift')
        exit()

    rootdir=dirname(sys.argv[1])
    df=pd.read_csv(sys.argv[1],dtype=str)

    rows=[]
    if sys.argv[2]=='replace':
        
        for i,row in df.iterrows():
            sub=row['src_subject_id']

            if len(sub)>=7 and len(sub)<=9:
                # all ids like AB12345_1
                _sub=sub[:7]
                if '_' not in _sub and not validate(_sub):
                    # all ids like [AB12345]
                    _sub=sub[1:8]
                    if not validate(_sub):
                        continue

                # ab12345-->AB12345
                _sub=_sub.upper()
                
                row['src_subject_id']=_sub
                rows.append(row)


        df1=pd.DataFrame(rows,columns=df.columns)
        df1.drop(columns=['redcap_id','ndar_penncnb01_complete'],inplace=True)
        df1.insert(loc=0,column='subjectkey',value='')
        df1.to_csv(pjoin(rootdir,f'ampscz_ids_{datestamp}.csv'),index=False)


    if sys.argv[2]=='shift':

        off='/data/predict1/data_from_nda/$/PHOENIX/PROTECTED/date_offset.csv'
        d1=pd.read_csv(off.replace('$','Pronet'))
        d2=pd.read_csv(off.replace('$','Prescient'))
        dshift=pd.concat((d1,d2)).set_index('subject')
        
        new_dates=['']*df.shape[0]
        for i,row in df.iterrows():
            shift=int(dshift.loc[row['src_subject_id'],'days'])

            new_date=datetime.strptime(row['interview_date'],'%m/%d/%Y')+timedelta(days=shift)
            new_dates[i]=new_date.strftime('%m/%d/%Y')

        
        df1=df.copy()
        df1['interview_date']=new_dates
        df1.to_csv(pjoin(rootdir,f'date_shifted_{datestamp}.csv'),index=False)


