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


def get_survey_mri_df_pronet(ampscz_id: str, fields_to_check: list,
                             timepoint: str) -> str:
    site = ampscz_id[:2]

    data_location = '/data/predict/data_from_nda'
    pronet_root = Path(data_location) / 'Pronet'
    pronet_protected = pronet_root / 'PHOENIX' / 'PROTECTED'
    study_protected = pronet_protected / f'Pronet{site}'
    study_protected_raw = study_protected / 'raw'

    subject_protected_raw = study_protected_raw / ampscz_id
    survey_protected_raw = subject_protected_raw / 'surveys'
    survey_json_path = survey_protected_raw / f'{ampscz_id}.Pronet.json'

    with open(survey_json_path, 'r') as fp:
        data = json.load(fp)
        
    df = pd.DataFrame(data)

    if timepoint == 'baseline':
        df = df[df['redcap_event_name'] == 'baseline_arm_1']
    elif timepoint == 'followup':
        df = df[df['redcap_event_name'] == 'month_2_arm_1']


    mri_avail_df = df[df.chrmri_consent != '']
    df_tmp = mri_avail_df[
            ['redcap_event_name'] +
            [x for x in df.columns if x in fields_to_check]
        ].set_index('redcap_event_name').T

    # update Fail binary variables to 3
    df_tmp.loc['chrmri_confirm'] = df_tmp.loc['chrmri_confirm'].apply(
            lambda x: '1' if x == '-3' else x)
    for binary_field in ['chrmri_metal',
                         'chrmri_physicalmetal',
                         'chrmri_dental']:
        df_tmp.loc[binary_field] = df_tmp.loc[binary_field].apply(
                lambda x: '1' if x == '1' else '3')

    out_df = df_tmp.isin(['1', '2', '']).all(axis=0)

    return out_df.loc[timepoint]


def get_survey_mri_df_prescient(ampscz_id: str, fields_to_check: list,
                                timepoint: str) -> str:

    if timepoint == 'baseline':
        timepoint = 2
    elif timepoint == 'followup':
        timepoint = 4

    site = ampscz_id[:2]

    data_location = '/data/predict/data_from_nda'
    prescient_root = Path(data_location) / 'Prescient'
    prescient_protected = prescient_root / 'PHOENIX' / 'PROTECTED'
    site = 'ME'
    study_protected = prescient_protected / f'Prescient{site}'
    study_protected_raw = study_protected / 'raw'

    subject_protected_raw = study_protected_raw / ampscz_id
    survey_protected_raw = subject_protected_raw / 'surveys'

    mri_run_sheet = survey_protected_raw / f'{ampscz_id}_mri_run_sheet.csv'

    mri_df = pd.read_csv(mri_run_sheet)
    mri_df = mri_df[mri_df.visit == timepoint]
    # ignore -3
    df_tmp = mri_df.T

    # -3 columns
    to_ignore_col_names = mri_df[(df_tmp == -3).T].dropna(axis=1).columns

    mri_df = mri_df.drop(to_ignore_col_names, axis=1).fillna('')

    out_df = mri_df[
            [x for x in fields_to_check if x in mri_df.columns]].T.isin(
                    [1, 2, '']).all(axis=0)
    return out_df.iloc[0]


def get_pass_fail_survey_mri_df(ampscz_id: str, timepoint: str) -> bool:
    '''

    Key Arguments:
        ampscz_id:
        timepoint: 'baseline' or 'followup'
    '''
    fields_to_check = [
            'chrmri_confirm', 'chrmri_metal',
            'chrmri_physicalmetal', 'chrmri_dental', 'chrmri_consent',
            'chrmri_aahscout',
            'chrmri_calib_ge', 'chrmri_calib_ge_2', 'chrmri_calib_ge_3',
            'chrmri_localizeraligned', 'chrmri_localizerseq',
            'chrmri_localizerseq_ge',
            'chrmri_dmap', 'chrmri_dmap2', 'chrmri_dmap3',
            'chrmri_dmap_qc', 'chrmri_dmap_qc_2', 'chrmri_dmap_qc_3',
            'chrmri_dmpa', 'chrmri_dmpa2', 'chrmri_dmpa3',
            'chrmri_dmpa_qc', 'chrmri_dmpa_qc_2', 'chrmri_dmpa_qc_3',
            'chrmri_t1', 'chrmri_t1_qc',
            'chrmri_t2', 'chrmri_t2_qc', 'chrmri_t2_ge', 'chrmri_t2_qc_ge',
            'chrmri_dmri126', 'chrmri_dmri126_qc',
            'chrmri_dmri176', 'chrmri_dmri176_qc',
            'chrmri_dmri_b0', 'chrmri_dmri_b0_2',
            'chrmri_dmri_b0_qc', 'chrmri_dmri_b0_qc_2',
            'chrmri_rfmriap', 'chrmri_rfmriap2',
            'chrmri_rfmriap2_qc', 'chrmri_rfmriap_qc',
            'chrmri_rfmriap_ref_num', 'chrmri_rfmriap_ref_num_2',
            'chrmri_rfmriap_ref_qc', 'chrmri_rfmriap_ref_qc_2',
            'chrmri_rfmripa', 'chrmri_rfmripa2',
            'chrmri_rfmripa2_qc', 'chrmri_rfmripa_qc',
            'chrmri_rfmripa_ref_num', 'chrmri_rfmripa_ref_num_2',
            'chrmri_rfmripa_ref_qc', 'chrmri_rfmripa_ref_qc_2'
            ]

    if get_study(ampscz_id) == 'Pronet':
        qc_var = get_survey_mri_df_pronet(ampscz_id,
                                          fields_to_check,
                                          timepoint)
        return qc_var

    elif get_study(ampscz_id) == 'Prescient':
        qc_var = get_survey_mri_df_prescient(ampscz_id,
                                             fields_to_check,
                                             timepoint)
        return qc_var
