#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob
from os.path import isfile,basename,abspath,dirname,join as pjoin


# this function should have knowledge of dict1
def get_value(var,event):

    for d in dict1:
        if d['redcap_event_name']==event:
            try:
                return d[var]
            except KeyError:
                break

    return ''


def months_since_consent(interview,consent):
    age= datetime.strptime(interview,'%Y-%m-%d')-datetime.strptime(consent,'%Y-%m-%d')
    return round(age.days/30)


def nda_date(redcap_date):
    if redcap_date=='':
        # REDCap missing: 1909-09-09
        # REDCap N/A: 1903-03-03
        return '1903-03-03'

    Y=redcap_date[:4]
    m,d=redcap_date[5:].split('-')
    new_date=f'{m}/{d}/{Y}'

    return new_date


def populate():

    src_subject_id=basename(file).split('.')[0]
    try:
        dfshared.loc[src_subject_id]
    except KeyError:
        return


    if dfshared.loc[src_subject_id,'phenotype']=='CHR':
        arm=1
    else:
        if prefix=='chrpas':
            # no assignment of premorbid_adjustment_scale to HC
            return
        else:
            arm=2


    interview_date=get_value(f'{prefix}_interview_date',f'{event}_arm_{arm}')
    if interview_date in ['','-3','-9','1903-03-03','1909-09-09']:
        # either no data in this form or the subject has not reached the event yet
        return

    # get shared variables
    df.at[row,'src_subject_id']=src_subject_id
    for v in ['subjectkey','sex']:
        df.at[row,v]=dfshared.loc[src_subject_id,v]


    # get form specific variables
    df.at[row,'interview_date']=nda_date(interview_date)
    df.at[row,'visit']=event
    
    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')
    months=months_since_consent(interview_date,chric_consent_date)
    df.at[row,'interview_age']=dfshared.loc[src_subject_id,'interview_age']+months

    for v in columns:
        if prefix in v and v not in csv_columns:
            value=get_value(v,f'{event}_arm_{arm}')

            if definition.loc[v,'DataType']=='Integer':
                if value=='':
                    # NDA missing: -300
                    # NDA N/A: -900
                    value='-300'
                elif value in ['-3','-9']:
                    value+='00'
                elif '.' in value:
                    value=value.split('.')[-1]

            elif definition.loc[v,'DataType']=='String':
                if value in ['-3','-9']:
                    value=''

            df.at[row,v]=value


    missing=get_value(f'{prefix}_missing',f'{event}_arm_{arm}')
    if missing=='':
        # not clicked
        missing='0'
    df.at[row,'ampscz_missing']=missing
    if missing=='1':
        value=df.at[row,'ampscz_missing_spec']=get_value(f'{prefix}_missing_spec',f'{event}_arm_{arm}')

        if len(value)>1:
            # two letter missing codes: W1,W2,W3,... M1,M2,M3,...
            df.at[row,'ampscz_missing_spec']=value[1]
        else:
            # single number missing code: 1,2,3,...
            df.at[row,'ampscz_missing_spec']=value

    else:
        df.at[row,'ampscz_missing_spec']=''

    # return df


    features_file=pjoin(dirname(file),'premorbid_adjustment_scale.csv')

    if not isfile(features_file):
        return

    df1=pd.read_csv(features_file)
    df1.set_index(['variable', 'redcap_event_name'],inplace=True)
    
    for v in csv_columns:
        df.at[row,v]=df1.loc[v,f'{event}_arm_{arm}']['value']



if __name__=='__main__':

    parser= argparse.ArgumentParser("Make data frame to submit to NDA")
    parser.add_argument("--dict", required=True,
        help="/path/to/nda/submission/template.csv")
    parser.add_argument("--root", required=True,
        help="/path/to/PHOENIX/GENERAL/")
    parser.add_argument("-t","--template", required=True,
        help="*/processed/*/surveys/*.Pronet.json")
    parser.add_argument("-o","--output", required=True,
        help="/path/to/submission_ready.csv")
    parser.add_argument("-e","--event", required=True,
        help="Event name: screening, baseline, month_1, etc.")
    parser.add_argument("-p","--prefix", required=True,
        help="Variable name prefix e.g. chrnsipr, chrpgis, chrassist, etc.")
    parser.add_argument("--shared", required=True,
        help="/path/to/ndar_subject01*.csv containing fields shared across NDA dicts")

    
    args= parser.parse_args()
    
    # load shared ndar_subject01
    with open(args.shared) as f:
        title,df=f.read().split('\n',1)

        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(df)
        
        dfshared=pd.read_csv(name)
        remove(name)
        dfshared.set_index('src_subject_id',inplace=True)
    
    
    # load NDA dictionary
    with open(args.dict) as f:
        title,df=f.read().split('\n',1)

        prefix=args.prefix
        event=args.event

        columns=['subjectkey','src_subject_id','interview_date','interview_age','sex','visit']

        pas_columns=['chrpas_pmod_child1','chrpas_pmod_child2','chrpas_pmod_child3','chrpas_pmod_child4',
           'chrpas_pmod_adol_early1','chrpas_pmod_adol_early2','chrpas_pmod_adol_early3',
           'chrpas_pmod_adol_early4','chrpas_pmod_adol_early5',
           'chrpas_pmod_adol_late1','chrpas_pmod_adol_late2','chrpas_pmod_adol_late3',
           'chrpas_pmod_adol_late4','chrpas_pmod_adol_late5',
           'chrpas_pmod_adult1','chrpas_pmod_adult2','chrpas_pmod_adult3v1','chrpas_pmod_adult3v3']

        preiq_columns='chrpreiq_reading_task chrpreiq_total_raw chrpreiq_standard_score'.split()

        if prefix=='chrpas':

            csv_columns='chrpas_childhood_subtotal chrpas_early_adolescence_subtotal \
                chrpas_late_adolescence_subtotal chrpas_adulthood_subtotal \
                chrpas_total_score_only_childhood chrpas_total_score_upto_early_adolescence \
                chrpas_total_score_upto_late_adolescence chrpas_total_score_upto_adulthood'.split()

            columns=columns+pas_columns+csv_columns

        elif prefix=='chrpreiq':
            
            csv_columns=[]
            columns=columns+preiq_columns
            
        columns+=['ampscz_missing','ampscz_missing_spec']

        
        # save the remaining template
        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(','.join(columns))
        
        # load template as DataFrame
        df=pd.read_csv(name)
        columns=df.columns.values
        remove(name)
        
        # load template definition
        definition=pd.read_csv(args.dict.replace('_template','_definitions'))
        definition.set_index('ElementName',inplace=True)

    dir_bak=getcwd()
    chdir(args.root)
    
    files=glob(args.template)
    for row,file in enumerate(files):
        
        print('Processing',file)
        
        with open(file) as f:
            dict1=json.load(f)

        populate()

    chdir(dir_bak)
    
    _,name=mkstemp()
    df.to_csv(name,index=False)
    
    with open(name) as f:
        data=f.read()
    remove(name)
    
    with open(args.output,'w') as f:
        f.write(title+'\n'+data)
    
    print('Generated',abspath(args.output))
    
