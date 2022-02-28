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


def _latest_mtime(p: Path) -> str:
    print('Finding modification time of', p)	

    latest = -1
    for file in p.rglob('*'):
        if file.is_file():
            mtime = file.stat().st_mtime
            if mtime > latest:
                latest = mtime
    
    return datetime.fromtimestamp(latest).strftime('%Y-%m-%d')


def get_summary_from_phoenix(phoenix_dir: Path) -> pd.DataFrame:
    '''Get summary from the PHOENIX structure'''
    
    subject_paths = list(phoenix_dir.glob('*/*/*/*'))
    
    df = pd.DataFrame({'p': subject_paths})
    df['subject_id'] = df.p.apply(lambda x: x.name)
    df['site'] = df.p.apply(lambda x: x.parent.parent.name[-2:])
    df['mtime']= df.p.apply(lambda x: _latest_mtime(x))
    df['level0'] = df.p.apply(lambda x: x.parent.parent.parent.name)
    df['level1'] = df.p.apply(lambda x: x.parent.name)

    # surveys
    df['surveys'] = df.p.apply(
        lambda x: (_is_file(x, 'surveys', '*Pronet.json') or
                  _is_file(x, 'surveys', '*.csv')))
    
    # PennCNB
    df['cnb'] = df.p.apply(lambda x: _is_file(x, 'surveys', '*UPENN.json'))
    df['cnb_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'surveys', 
        suffix='PennCNB'))
    

    # eeg
    df['eeg'] = df.p.apply(lambda x: _is_file(x, 'eeg', '*zip'))
    df['eeg_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'eeg'))

    # actigraphy
    df['actigraphy'] = df.p.apply(lambda x: _is_file(x, 'actigraphy', '*cwa'))
    df['actigraphy_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'actigraphy'))

    # mri
    df['mri'] = df.p.apply(lambda x: (_is_dir(x, 'mri', '*') or
                                     _is_file(x, 'mri', '*.zip')))
    df['mri_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'mri'))

    # A/V
    df['interview_audio'] = df.p.apply(
        lambda x: _is_file(x, 'interviews', '*/*interviewMonoAudioQC*.csv'))
    df['interview_video'] = df.p.apply(
        lambda x: _is_file(x, 'interviews', '*/*interviewVideoQC*.csv'))
    df['interview_transcript'] = df.p.apply(
        lambda x: _is_file(x, 'interviews', '*/*interviewRedactedTranscriptQC*.csv'))
    df['interview_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'interviews'))

    # mindlamp
    df['mind_phone'] = df.p.apply(
        lambda x: _get_count(x, 'phone', '*_activity_*json'))
    df['mind_sensor'] = df.p.apply(
        lambda x: _get_count(x, 'phone', '*_sensor_*json'))
    df['mind_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'phone'))
    
    
    return df
    

def phoenix_files_status(phoenix_dir, out_dir):

    print(f'\nFinding files status of {phoenix_dir}\n')

    df = get_summary_from_phoenix(phoenix_dir)

    dtypes= df.columns[6:].values
    groups= df.groupby('subject_id')
    for subject,group in groups:
        df_tmp= {}

        df_tmp['subject_id']= subject
        site= group['site'].values[0]
        df_tmp['site']= site
        df_tmp['mtime']= group['mtime'].max()
        
        for d in dtypes:
            for _,row in group.iterrows():
                dname= '_'.join([d, row['level1'], row['level0']])
            
                df_tmp[dname]= row[d]

        # one subject belongs to only one site
        # so it is safe to take the first site value as the site of that subject
        subject_series_tmp= pd.DataFrame(df_tmp, index=[0])
        
        # https://gist.github.com/tashrifbillah/cea43521588adf127cae79353ae09968
        # suggestion from Tashrif to link outputs to DPdash
        subject_df_tmp = pd.DataFrame({
            'day': [1],
            'reftime': '',
            'timeofday': '',
            'weekday': ''
        })
        
        subject_df_tmp = pd.concat([subject_df_tmp, subject_series_tmp], axis=1)
        out_file = f"{site}-{subject}-flowcheck-day1to1.csv"
        subject_df_tmp.to_csv(out_dir/out_file, index=False)


def _get_count(root: Path, subdir: str, pattern: str) -> int:
    '''get number of files and directories that mattch glob pattern'''
    return len(list((root / subdir).glob(pattern)))


def _get_dir_count(root: Path, subdir: str, pattern: str) -> int:
    '''get number of directories that mattch glob pattern'''
    return len([x for x in (root / subdir).glob(pattern) if x.is_dir()])


def _get_file_count(root: Path, subdir: str, pattern: str) -> int:
    '''get number of files that mattch glob pattern'''
    return len([x for x in (root / subdir).glob(pattern) if x.is_file()])


def _is_file(root: Path, subdir: str, pattern: str) -> int:
    '''check if there is at least one file matching the given pattern'''
    return min(_get_file_count(root, subdir, pattern),1)


def _is_dir(root:Path, subdir: str, pattern: str) -> int:
    '''check if there is at least one directory matching the pattern'''
    return min(_get_dir_count(root, subdir, pattern),1)


def _is_scansheet(root:Path, subdir: str, suffix: str= None) -> int:
    '''check if there is a scan sheet for a datatype (subdir)'''
    if not suffix:
        suffix= subdir

    return min(_get_count(
            root, subdir, f'{root.name}.*.Run_sheet_{suffix}.csv'),1)


if __name__=='__main__':
    phoenix_files_status(pronet_phoenix_dir, pronet_status_dir)
    phoenix_files_status(prescient_phoenix_dir, prescient_status_dir)

