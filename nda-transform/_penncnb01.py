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
        df1.drop(columns='''cnb_digsym_dsmcrrtv2
                            cnb_pllt_plltclothingcor1
                            cnb_pllt_plltinsectcor1
                            cnb_pllt_plltearthformationcor1
                            cnb_pllt_plltflowercor1
                            cnb_pllt_plltclothingcor2
                            cnb_pllt_plltinsectcor2
                            cnb_pllt_plltearthformationcor2
                            cnb_pllt_plltflowercor2
                            cnb_pllt_plltclothingcor3
                            cnb_pllt_plltinsectcor3
                            cnb_pllt_plltearthformationcor3
                            cnb_pllt_plltflowercor3
                            cnb_pllt_plltseme1
                            cnb_pllt_plltsema1
                            cnb_pllt_plltsere1
                            cnb_pllt_plltsera1
                            cnb_pllt_plltseme2
                            cnb_pllt_plltsema2
                            cnb_pllt_plltsere2
                            cnb_pllt_plltsera2
                            cnb_pllt_plltseme3
                            cnb_pllt_plltsema3
                            cnb_pllt_plltsere3
                            cnb_pllt_plltsera3
                            cnb_pllt_plltbirdcor1
                            cnb_pllt_plltmetalcor1
                            cnb_pllt_pllttoolcor1
                            cnb_pllt_plltsportcor1
                            cnb_pllt_plltbirdcor2
                            cnb_pllt_plltmetalcor2
                            cnb_pllt_pllttoolcor2
                            cnb_pllt_plltsportcor2
                            cnb_pllt_plltbirdcor3
                            cnb_pllt_plltmetalcor3
                            cnb_pllt_pllttoolcor3
                            cnb_pllt_plltsportcor3
                            cnb_pllt_plltanimalcor1
                            cnb_pllt_plltjewelcor1
                            cnb_pllt_plltsheltercor1
                            cnb_pllt_plltjobcor1
                            cnb_pllt_plltanimalcor2
                            cnb_pllt_plltjewelcor2
                            cnb_pllt_plltsheltercor2
                            cnb_pllt_plltjobcor2
                            cnb_pllt_plltanimalcor3
                            cnb_pllt_plltjewelcor3
                            cnb_pllt_plltsheltercor3
                            cnb_pllt_plltjobcor3
                            cnb_pllt_plltinstrumentcor1
                            cnb_pllt_plltspicecor1
                            cnb_pllt_plltfuelcor1
                            cnb_pllt_plltvegetablecor1
                            cnb_pllt_plltinstrumentcor2
                            cnb_pllt_plltspicecor2
                            cnb_pllt_plltfuelcor2
                            cnb_pllt_plltvegetablecor2
                            cnb_pllt_plltinstrumentcor3
                            cnb_pllt_plltspicecor3
                            cnb_pllt_plltfuelcor3
                            cnb_pllt_plltvegetablecor3
                            cnb_mpract_comment
                            cnb_spcptn90_comment
                            cnb_er40_comment
                            cnb_sfnb2_comment
                            cnb_digsym_comment
                            cnb_volt_comment
                            cnb_sctap_comment
                            cnb_pllt_comment
                            session_system_status
                            cnb_mpract_system_status
                            cnb_spcptn90_system_status
                            cnb_er40_system_status
                            cnb_sfnb2_system_status
                            cnb_digsym_system_status
                            cnb_volt_system_status
                            cnb_sctap_system_status
                            cnb_pllt_system_status
                            cnb_mpract_status
                            cnb_spcptn90_status
                            cnb_er40_status
                            cnb_sfnb2_status
                            cnb_digsym_status
                            cnb_volt_status
                            cnb_sctap_status
                            cnb_pllt_status
                            siteid
                            visitid
                            redcap_id
                            ndar_penncnb01_complete
                            webcnp_complete'''.split(),inplace=True)
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


