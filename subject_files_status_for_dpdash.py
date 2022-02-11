#!/usr/bin/env python

# cleaned up Kevin's work to make DPdash compatible files
# inserted codes for mtime: the latest time when a subject's data was downloaded

from pathlib import Path
import pandas as pd
import numpy as np
from datetime import time, timedelta, datetime, date

flow_test_root = Path('/data/predict/kcho/flow_test')
pronet_phoenix_dir = flow_test_root / 'Pronet/PHOENIX'
prescient_phoenix_dir = flow_test_root / 'Prescient/PHOENIX'

pronet_status_dir = flow_test_root/ 'Pronet_status'
prescient_status_dir = flow_test_root/ 'Prescient_status'


from os import stat
from os.path import isfile
from datetime import datetime

def _latest_mtime(p):
    
    print('Finding modification time of',p)	

    latest= -1
    for file in p.rglob('*'):
        if file.is_file():
            mtime= file.stat().st_mtime
            if mtime>latest:
                latest= mtime
    
    return datetime.fromtimestamp(latest).strftime('%Y-%m-%d')


def get_summary_from_phoenix(phoenix_dir: Path) -> pd.DataFrame:
    '''Get summary from the PHOENIX structure'''
    
    subject_paths = list(phoenix_dir.glob('*/*/*/*'))
    
    df = pd.DataFrame({'p': subject_paths})
    df['subject'] = df.p.apply(lambda x: x.name)
    df['site'] = df.p.apply(lambda x: x.parent.parent.name)
    df['level0'] = df.p.apply(lambda x: x.parent.parent.parent.name)
    df['level1'] = df.p.apply(lambda x: x.parent.name)

    df['pronet_surveys'] = df.p.apply(lambda x: len(list((x / 'surveys').glob('*Pronet.json'))) > 0)
    df['upenn_surveys'] = df.p.apply(lambda x: len(list((x / 'surveys').glob('*UPENN.json'))) > 0)
    df['eeg'] = df.p.apply(lambda x: len(list((x / 'eeg').glob('*zip'))) > 0)
    df['eeg_ss'] = df.p.apply(lambda x: (x / 'eeg' / f'{x.name}.Pronet.Run_sheet_eeg.csv').is_file())
    df['actigraphy'] = df.p.apply(lambda x: len(list((x / 'actigraphy').glob('*zip'))) > 0)
    df['actigraphy_ss'] = df.p.apply(lambda x: (x / 'actigraphy' / f'{x.name}.Pronet.Run_sheet_actigraphy.csv').is_file())
    df['mri'] = df.p.apply(lambda x: len([x for x in (x / 'mri').glob('*') if x.is_dir()]) > 0)
    df['mri_ss'] = df.p.apply(lambda x: (x / 'mri' / f'{x.name}.Pronet.Run_sheet_mri.csv').is_file())
    df['interviews'] = df.p.apply(lambda x: len([x for x in (x / 'interviews').glob('*') if x.is_dir()]) > 0)
    df['interviews_ss'] = df.p.apply(lambda x: (x / 'interviews' / f'{x.name}.Pronet.Run_sheet_interviews.csv').is_file())
    df['mind_phone'] = df.p.apply(lambda x: len( [x for x in (x / 'phone').glob('*_activity_*json')] ))
    df['mind_audio'] = df.p.apply(lambda x: len( [x for x in (x / 'phone').glob('*_activity_*_sound_*.mp3')] ))
    df['mind_sensor'] = df.p.apply(lambda x: len( [x for x in (x / 'phone').glob('*_sensor_*json')] ))
    
    df['mtime']= df.p.apply(lambda x: _latest_mtime(x))
    
    return df
    

def phoenix_files_status(phoenix_dir, out_dir):

    print(f'\nFinding files status of {phoenix_dir}\n')

    df = get_summary_from_phoenix(phoenix_dir)

    df_pivot = pd.pivot_table(df, index=['subject', 'site', 'mtime'], 
        columns=['level0', 'level1'], fill_value=False).astype(int)

    for (subject, site, mtime), row in df_pivot.iterrows():
        df_tmp = row.reset_index()
        df_tmp.columns = ['datatype', 'level0', 'level1', 'count']
        df_tmp_pivot = pd.pivot_table(df_tmp, columns=['datatype', 'level0', 'level1']).reset_index()
        df_tmp_pivot['col'] = df_tmp_pivot['datatype'] + '_' + \
                              df_tmp_pivot['level1'] + '_' + \
                              df_tmp_pivot['level0']
        subject_series_tmp = df_tmp_pivot.set_index('col')[0]
        
        subject_series_tmp['mtime']= mtime
        subject_series_tmp['site']= site[-2:]
        
        # https://gist.github.com/tashrifbillah/cea43521588adf127cae79353ae09968
        # suggestion from Tashrif to link outputs to DPdash
        subject_df_tmp = pd.DataFrame({
            'day': [1],
            'reftime': '',
            'timeofday': '',
            'weekday': ''
        })
        
        subject_df_tmp = pd.concat([subject_df_tmp, pd.DataFrame(subject_series_tmp).T], axis=1)
        
        out_file = f"{site[-2:]}-{subject}-flowcheck-day1to1.csv"

        subject_df_tmp.to_csv(out_dir/out_file, index=False)



if __name__=='__main__':
    phoenix_files_status(pronet_phoenix_dir, pronet_status_dir)
    phoenix_files_status(prescient_phoenix_dir, prescient_status_dir)

