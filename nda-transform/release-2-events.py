#!/usr/bin/env python

import pandas as pd

devents=pd.read_csv('/data/predict1/to_nda/nda-submissions/release-2-events')
redcap_nda=pd.read_csv('/data/predict1/utility/nda-transform/redcap_nda_form_mapping.csv')
redcap_nda.set_index('redcap_form_name',inplace=True)

for i,row in devents.iterrows():
    event=row['event'].split('_arm_')[0]
    form=row['form']
    
    try:
        df=redcap_nda.loc[ [form] ]

        for _,_row in df.iterrows():
            addl_arg=_row['addl_arg']

            if pd.isna(addl_arg):
                print('-f',_row['nda_short_name'],'-e',event)
            else:
                print('-f',_row['nda_short_name'],'-e',event,'-p',addl_arg)
        
    except KeyError:
        pass

