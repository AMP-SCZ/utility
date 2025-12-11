#!/usr/bin/env python

import pandas as pd
import sys

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage:
    {__file__} /data/predict1/to_nda/nda-submissions/release-4-events generate
    {__file__} /data/predict1/to_nda/nda-submissions/release-4-events combine
    {__file__} /data/predict1/to_nda/nda-submissions/release-2-events submit

This script gives nicely formatted commands to include in release-?-events.sh.''')
    exit(0)


devents=pd.read_csv(sys.argv[1])
# devents=pd.read_csv('/data/predict1/to_nda/nda-submissions/release-2-events')
# devents=pd.read_csv('/data/predict1/to_nda/nda-submissions/release-4-events')
# to group same form together
# devents.sort_values('form',inplace=True)
redcap_nda=pd.read_csv('/data/predict1/utility/nda-transform/redcap_nda_form_mapping.csv')
redcap_nda.set_index('redcap_form_name',inplace=True)

for i,row in devents.iterrows():
    event=row['event'].split('_arm_')[0]
    form=row['form']
    
    try:
        df=redcap_nda.loc[ [form] ]

        for _,_row in df.iterrows():
            addl_arg=_row['addl_arg']
            short_name=_row['nda_short_name']
            
            if sys.argv[2]=='generate':
                cmd=f'./generate.sh -n $n -e {event:14} -f {short_name:16} '
                
                if not pd.isna(addl_arg):
                    cmd+=f'-p {addl_arg}'
                
            elif sys.argv[2]=='combine':
                cmd=f'./combine_networks.sh -e {event:14} -f {short_name:16} '

            elif sys.argv[2]=='submit':
                cmd=f'./combine_networks.sh -u tbillah -e {event:14} -f {short_name:16} '

            print(cmd)
            
    except KeyError:
        pass

