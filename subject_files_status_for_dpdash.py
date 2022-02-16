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
    df['subject'] = df.p.apply(lambda x: x.name)
    df['site'] = df.p.apply(lambda x: x.parent.parent.name)
    df['level0'] = df.p.apply(lambda x: x.parent.parent.parent.name)
    df['level1'] = df.p.apply(lambda x: x.parent.name)

    # surveys
    df['surveys'] = df.p.apply(
        lambda x: (_is_file(x, 'surveys', '*Pronet.json') or
                  _is_file(x, 'surveys', '*.csv')))
    df['upenn_surveys'] = df.p.apply(
        lambda x: _is_file(x, 'surveys', '*UPENN.json'))

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
    df['interviews'] = df.p.apply(
        lambda x: _is_file(x, 'interviews', '*.csv'))
    df['interviews_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'interviews'))

    # mindlamp
    df['mind_phone'] = df.p.apply(
        lambda x: _get_count(x, 'phone', '*_activity_*json'))
    df['mind_sensor'] = df.p.apply(
        lambda x: _get_count(x, 'phone', '*_sensor_*json'))
    
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
        df_tmp_pivot = pd.pivot_table(
                df_tmp, columns=['datatype', 'level0', 'level1']).reset_index()
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
        
        subject_df_tmp = pd.concat(
            [subject_df_tmp, pd.DataFrame(subject_series_tmp).T], axis=1)
        out_file = f"{site[-2:]}-{subject}-flowcheck-day1to1.csv"
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


def _is_file(root: Path, subdir: str, pattern: str) -> bool:
    '''check if there is at least one file matching the given pattern'''
    return _get_file_count(root, subdir, pattern) > 0


def _is_dir(root:Path, subdir: str, pattern: str) -> bool:
    '''check if there is at least one directory matching the pattern'''
    return _get_dir_count(root, subdir, pattern) > 0


def _is_scansheet(root:Path, subdir: str) -> bool:
    '''check if there is a scan sheet for a datatype (subdir)'''
    return _get_count(
            root, subdir, f'{root.name}.*.Run_sheet_{subdir}.csv') > 0


if __name__=='__main__':
    phoenix_files_status(pronet_phoenix_dir, pronet_status_dir)
    phoenix_files_status(prescient_phoenix_dir, prescient_status_dir)

