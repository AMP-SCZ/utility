import sys
from pathlib import Path
CODE_ROOT = Path(__file__).parent.parent
sys.path.append(str(CODE_ROOT))
from subject_files_status_for_dpdash2 import get_mri_status, \
        get_value_from_dict
import pandas as pd
import json


def test_import():
    pass


def get_info(subject, timepoint):
    nda_root = Path('/data/predict1/data_from_nda/')
    surveys = nda_root.glob(
            f'P*/PHOENIX/PROTECTED/*/raw/{subject}/surveys/'
            f'*.P*.json')
    s = next(surveys)
    # subject = s.parent.parent.name
    with open(s) as f:
        dict1=json.load(f)

    consent_date = get_value_from_dict(
            dict1, 'screening', 'chric_consent_date')

    # extract and join CHR and HC arms
    dict2=[]
    for d in dict1:
        if timepoint in d['redcap_event_name']:
            dict2.append(d)
    dict1 = dict2

    return consent_date, dict1


def test_run_get_mri_status_test_one():
    # timepoint = 'baseline'
    timepoint = 'month_2'
    nda_root = Path('/data/predict1/data_from_nda/')
    network = 'Pronet'
    network = 'Prescient'
    subject = 'ME79913'
    subject = 'SF14052'
    subject = 'ST18995'
    subject = 'ST91452'
    # subject = 'LS55502'
    surveys = (nda_root / network).glob(
            f'PHOENIX/PROTECTED/{network}??/raw/{subject}/surveys/'
            f'*.{network}.json')
    s = next(surveys)
    # subject = s.parent.parent.name
    with open(s) as f:
        dict1=json.load(f)

    consent_date = get_value_from_dict(dict1, 'screening', 'chric_consent_date')

    # extract and join CHR and HC arms
    dict2=[]
    for d in dict1:
        if timepoint in d['redcap_event_name']:
            dict2.append(d)
    dict1 = dict2
    dict_mri = get_mri_status(dict1, timepoint, consent_date, subject,
                              test=True)

    print(dict_mri)
    assert dict_mri['mri_data'] == 1


def test_run_get_mri_csv():
    print()
    timepoint = 'baseline'
    nda_root=Path('/data/predict1/data_from_nda/')
    network = 'Pronet'
    df = pd.read_csv(nda_root / 'combined-AMPSCZ-data_baseline-day1to1.csv')
    df = df[df.mri_data < 0]

    print(df[['subject_id', 'mri_data']])


def test_return_same_data():
    nda_root = Path('/data/predict1/data_from_nda/')
    mri_df = pd.read_csv(nda_root / 'MRI_ROOT/eeg_mri_count/mri_all_db.csv')
    mri_df = mri_df[mri_df.mri_data_exist == True]

    for index, row in mri_df.iterrows():
        timepoint = row['timepoint_text']
        try:
            consent_date, dict1 = get_info(row['subject'], timepoint)
        except ValueError:
            print(row['subject'], 'value error')
            continue
        except TypeError:
            print(row['subject'], 'type error')
            continue

        try:
            out_dict = get_mri_status(dict1, timepoint,
                                      consent_date, row['subject'])
        except ValueError:
            print(row['subject'], 'value error from get_mri_status')
            continue

        if out_dict['mri_data'] != 1:
            print(row)
            print(row['subject'], timepoint)
            print(out_dict)
            out_dict = get_mri_status(dict1, timepoint,
                                      consent_date, row['subject'],
                                      test=True)
            print('-'*100)


def test_run_get_mri_status_test_all():
    timepoint = 'baseline'
    timepoint = 'month_2'
    nda_root = Path('/data/predict1/data_from_nda/')
    network = 'Prescient'
    network = 'Pronet'
    subject = '*'
    surveys = (nda_root / network).glob(
            f'PHOENIX/PROTECTED/{network}??/raw/{subject}/surveys/'
            f'*.{network}.json')
    for s in surveys:
        # subject = s.parent.parent.name
        with open(s) as f:
            dict1=json.load(f)
        consent_date = get_value_from_dict(dict1, 'screening', 'chric_consent_date')

        # extract and join CHR and HC arms
        dict2=[]
        for d in dict1:
            if timepoint in d['redcap_event_name']:
                dict2.append(d)
        dict1 = dict2
        try:
            dict_mri = get_mri_status(dict1, timepoint, consent_date, subject,
                    test=True)
        except:
            print(s)

