#!/usr/bin/env python

import pandas as pd

devents=pd.read_csv('/data/predict1/to_nda/nda-submissions/release-2-events')
redcap_nda=pd.read_csv('/data/predict1/utility/nda-transform/redcap_nda_form_mapping.csv')
redcap_nda.set_index('redcap_form_name',inplace=True)

for i,row in devents.iterrows():
    event=row['event'].split('_arm_')[0]
    form=row['form']
    
    try:
        short_name=redcap_nda.loc[form,'nda_short_name']
        
        if isinstance(short_name, str):
            print('-f',short_name,'-e',event)
        else:
            # multiple rows for one form
            print('\t',form)
            continue
    except KeyError:
        pass

