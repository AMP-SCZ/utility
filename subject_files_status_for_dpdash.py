#!/usr/bin/env python

# cleaned up Kevin's work to make DPdash compatible files
# inserted codes for mtime: the latest time when a subject's data was downloaded

from pathlib import Path
import pandas as pd
import numpy as np
import re, sys
import json
from datetime import time, timedelta, datetime, date

# sys.arv[1] is the NDA_ROOT folder
flow_test_root = Path(sys.argv[1])
pronet_phoenix_dir = flow_test_root / 'Pronet/PHOENIX'
prescient_phoenix_dir = flow_test_root / 'Prescient/PHOENIX'

pronet_status_dir = flow_test_root/ 'Pronet_status'
prescient_status_dir = flow_test_root/ 'Prescient_status'

mri_root = flow_test_root / 'MRI_ROOT'
mri_qqc_root = mri_root / 'derivatives/quick_qc'


def _latest_mtime(p: Path) -> str:
    print('Finding modification time of', p)

    latest = -1
    for file in p.rglob('*'):
        if file.is_file():
            mtime = file.stat().st_mtime
            if mtime > latest:
                latest = mtime
    
    return datetime.fromtimestamp(latest).strftime('%Y-%m-%d')


def check_upenn_cnb(subject_raw_path: Path) -> bool:
    '''Check if there are SPLLT-A and NOSPLLT in the Penn CNB json file'''
    json_paths = list((subject_raw_path / 'surveys').glob('*UPENN.json'))

    if len(json_paths) == 0:  # No file
        return False

    with open(json_paths[0], 'r') as fp:
        data = json.load(fp)

    if len(data) != 2:
        return False

    session_batteries = [x['session_battery'] for x in data]
    spllta_check = 'SPLLT-A' in session_batteries
    nospllt_check = ('ProNET_NOSPLLT' in session_batteries or
                     'PRESCIENT_NOSPLLT_C1' in session_batteries)

    return spllta_check & nospllt_check


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
    df['cnb'] = df.p.apply(lambda x: check_upenn_cnb(x))
    df['cnb_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'surveys',
        suffix='PennCNB'))
    

    # eeg
    df['eeg'] = df.p.apply(lambda x: _is_file(x, 'eeg', '*zip'))
    df['eeg_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'eeg'))

    # actigraphy
    df['actigraphy'] = df.p.apply(lambda x: _is_file(x, 'actigraphy', '*cwa'))
    df['actigraphy_ss'] = df.p.apply(lambda x: _is_scansheet(x, 'actigraphy'))

    # mri
    df['mri'] = df.p.apply(lambda x: check_mri_and_qqc_result(x))
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
    

def check_mri_and_qqc_result(root: Path) -> int:
    '''Check if there is MRI data, and if it exist, represent QC results

    Key arguments:
        root: PHOENIX path of raw subject directory, Path.

    Returns:
        0: when there is no data, int.
        1: when there is MRI data, which failed MRI quick QC, int.
        2: when there is MRI data, which passed MRI quick QC, int.
        3: there is MRI data, QC not ran yet, int.
        4: when there is MRI data, which requires manual processing, int.

    '''

    if _is_dir(root, 'mri', '*'):
        sub_name = [x.name for x in
                    (root / 'mri').glob('*') if x.is_dir()][0]
    elif _is_file(root, 'mri', '*.zip'):
        sub_name = [x.name for x in (root / 'mri').glob('*.zip')][0]
    else:
        return 0  # no mri data

    name_sections = sub_name.split('_')

    if len(name_sections) != 6:
        return 4  # check name of the MRI file or directory

    # load QC result
    session_name = 'ses-' + ''.join(name_sections[2:]).split('.')[0]
    qqc_dir = mri_qqc_root / f'sub-{root.name}' / session_name
    qc_summary = qqc_dir / '00_qc_summary.csv'

    labels_to_check = ['Series count',
                       'Volume slice number comparison',
                       'Image orientation in anat',
                       'Image orientation in others',
                       'Bval comparison']

    if qc_summary.is_file():
        qc_df = pd.read_csv(qc_summary)
        qc_df = qc_df[qc_df[qc_df.columns[0]].isin(labels_to_check)]
        all_pass = (qc_df[qc_df.columns[1]] == 'Pass').all()

        if all_pass:
            return 2  # green
        else:
            return 1  # red

    else:
        return 3  # QC not ran yet


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
        subject_series_tmp.replace(0,'',inplace=True)
        
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
    return min(_get_file_count(root, subdir, pattern), 1)


def _is_dir(root:Path, subdir: str, pattern: str) -> int:
    '''check if there is at least one directory matching the pattern'''
    return min(_get_dir_count(root, subdir, pattern), 1)


def _is_scansheet(root:Path, subdir: str, suffix: str = None) -> int:
    '''check if there is a scan sheet for a datatype (subdir)'''
    if not suffix:
        suffix = subdir

    return min(_get_count(
            root, subdir, f'{root.name}.*.Run_sheet_{suffix}_*.csv'),1)


if __name__=='__main__':
    phoenix_files_status(pronet_phoenix_dir, pronet_status_dir)
    phoenix_files_status(prescient_phoenix_dir, prescient_status_dir)

