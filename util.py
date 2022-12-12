from datetime import datetime
from pathlib import Path
import pandas as pd
import json


def get_study(ampscz_id: str,
              data_from_nda_path: str = '/data/predict/data_from_nda/') -> str:
    '''Get name of the study based on the AMP-SCZ ID

    Key arguments:
        ampscz_id: AMP-SCZ ID, str.
        data_from_nda_path: Root path of Prescient and Pronet PHOENIX
                            directories, str

    Returns:
        str, either 'Prescient' or 'Pronet'
    '''

    site = ampscz_id[:2]
    data_from_nda_path = Path(data_from_nda_path)
    metadata_paths = data_from_nda_path.glob(
            '*/PHOENIX/GENERAL/*_metadata.csv')
    for metadata_path in metadata_paths:
        study = metadata_path.parent.parent.parent.parent.name
        if site in metadata_path.name:
            return study

    return None



def str_date_minus_str_date(date_str1: str, date_str2: str) -> int:
    '''Get time delta between dates in string:  -(date_str1 - date_str2)'''
    date1 = datetime.strptime(date_str1, '%Y-%m-%d')
    date2 = datetime.strptime(date_str2, '%Y-%m-%d')

    time_delta = -(date1 - date2)
    diff_days = time_delta.days

    return diff_days


def days_from_today_to_str_date(date_str: str) -> int:
    '''Get time delta from today to a date in string format'''
    diff_days = str_date_minus_str_date(datetime.today().strftime('%Y-%m-%d'),
                                        date_str)
    return diff_days


def check_file_delay(file: str, date_str: str) -> int:
    '''Get time delta from today to a date in string format'''
    if Path(file).is_file():
        return 1
    else:
        return days_from_today_to_str_date(date_str)


def get_guid_prescient(
        ampscz_id: str,
        PHOENIX_root: str = '/data/predict/data_from_nda/Prescient/PHOENIX') \
                -> str:
    '''Get GUID for a Prescient subject ID'''
    prescient_protected = Path(PHOENIX_root) / 'PROTECTED'
    site = ampscz_id[:2]
    study_protected = prescient_protected / f'Prescient{site}'
    study_protected_raw = study_protected / 'raw'

    subject_protected_raw = study_protected_raw / ampscz_id
    survey_protected_raw = subject_protected_raw / 'surveys'
    guid_form = survey_protected_raw / f'{ampscz_id}_guid_form.csv'

    df = pd.read_csv(guid_form)
    unique_guid_list = df['chrguid_guid'].unique()

    # make usre there is only one guid
    assert len(unique_guid_list) == 1, 'There is more than one GUID'
    guid = unique_guid_list[0]

    return guid


def get_guid_pronet(
        ampscz_id: str,
        PHOENIX_root: str = '/data/predict/data_from_nda/Pronet/PHOENIX') \
                -> str:
    '''Get GUID for a Pronet subject ID'''
    pronet_protected = Path(PHOENIX_root) / 'PROTECTED'
    site = ampscz_id[:2]
    study_protected = pronet_protected / f'Pronet{site}'
    study_protected_raw = study_protected / 'raw'

    subject_protected_raw = study_protected_raw / ampscz_id
    survey_protected_raw = subject_protected_raw / 'surveys'
    survey_json_path = survey_protected_raw / f'{ampscz_id}.Pronet.json'

    with open(survey_json_path, 'r') as fp:
        data = json.load(fp)

    df = pd.DataFrame(data)
    unique_guid_list = df['chrguid_guid'].map(
            lambda x: pd.NA if x=='' else x).dropna().unique()

    # make usre there is only one guid
    assert len(unique_guid_list) == 1, 'There is more than one GUID'
    guid = unique_guid_list[0]

    return guid


def get_guid(ampscz_id: str) -> str:
    '''Get GUID for a AMP-SCZ ID'''
    if get_study(ampscz_id) == 'Pronet':
        return get_guid_pronet(ampscz_id)
    elif get_study(ampscz_id) == 'Prescient':
        return get_guid_prescient(ampscz_id)
    else:
        return None
