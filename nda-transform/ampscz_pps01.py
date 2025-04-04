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
import re


# this function should have knowledge of dict1
def get_value(var,event):

    for d in dict1:
        if d['redcap_event_name']==event:
            try:
                return d[var]
            except KeyError:
                return ''
                
    # the subject has not reached the event yet
    return ''
    

def months_since_consent(interview,consent):
    age= datetime.strptime(interview,'%Y-%m-%d')-datetime.strptime(consent,'%Y-%m-%d')
    return round(age.days/30)


def nda_date(redcap_date):
    if redcap_date=='':
        # REDCap missing: 1909-09-09
        # REDCap N/A: 1903-03-03
        return '03/03/1903'

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
        arm=2


    interview_date=get_value(f'{prefix}_interview_date',f'{event}_arm_{arm}')
    if interview_date in ['','-3','1903-03-03','-9','1909-09-09']:
        # no data in this form
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
            
            vrange=definition.loc[v,'ValueRange']
            if not pd.isna(vrange):
                if '-300' in vrange or '-900' in vrange \
                    or '77' in vrange:
                    # NDA missing: -900
                    # NDA N/A: -300
                    if value=='-3':
                        value='-300'
                    elif value=='-9':
                        value='-900'

            if definition.loc[v,'DataType']=='Integer':
                try:
                    value=int(value)
                except ValueError:
                    value=''

            elif definition.loc[v,'DataType']=='String':
                if value in ['-3','-9']:
                    value=''
    
                size=definition.loc[v,'Size']
                if size:
                    # NDA definition of size is based on utf-8 encoding
                    value=value.encode('utf-8')[:int(size)].decode('utf-8','ignore')

                if '\n' in value:
                    value=value.replace('\n',' ')
                if '\r' in value:
                    value=value.replace('\r','')

            elif definition.loc[v,'DataType']=='Date':
                value=nda_date(value)

            elif definition.loc[v,'DataType']=='Float':
                try:
                    value=round(float(value),3)
                except ValueError:
                    pass

            df.at[row,v]=value


    missing=get_value(f'{prefix}_missing',f'{event}_arm_{arm}')
    if missing=='':
        # not clicked
        missing='0'
    df.at[row,'ampscz_missing']=missing
    if missing=='1':
        df.at[row,'ampscz_missing_spec']=get_value(f'{prefix}_missing_spec',f'{event}_arm_{arm}')[1]
    else:
        df.at[row,'ampscz_missing_spec']=''

    # return df

    features_file=pjoin(dirname(file),'psychosis_polyrisk_score.csv')

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
    args.dict=args.dict.replace('_template.csv','_definitions.csv')
    title=re.search('/(.+?)01_definitions.csv',args.dict).group(1)
    definition=pd.read_csv(args.dict)
    definition.set_index('ElementName',inplace=True)
    
    prefix=args.prefix
    event=args.event

    columns=['subjectkey','src_subject_id','interview_date','interview_age','sex','visit']
    for c in definition.index:
        if prefix in c:
            columns.append(c.strip())
    
    csv_columns='chrpps_sum1,chrpps_sum2,chrpps_sum7,chrpps_sum8,chrpps_sum9,chrpps_sum10,chrpps_sum11,chrpps_sum12,chrpps_sum13,chrpps_sum14,\
chrpps_sum6,chrpps_total,chrpps_pa_sum,chrpps_sa_sum,chrpps_ea_sum,chrpps_en_sum,chrpps_pn_sum'.split(',')

    columns+=['ampscz_missing','ampscz_missing_spec']
    
    # save the remaining template
    _,name=mkstemp()
    with open(name,'w') as fw:
        fw.write(','.join(columns))
    
    # load template as DataFrame
    df=pd.read_csv(name)
    columns=df.columns.values
    remove(name)


    dir_bak=getcwd()
    chdir(args.root)
    
    files=glob(args.template)
    for row,file in enumerate(files):
        
        print('Processing',file)
        
        with open(file) as f:
            dict1=json.load(f)

        populate()


    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    chdir(dir_bak)
    
    _,name=mkstemp()
    df.to_csv(name,index=False)
    
    with open(name) as f:
        data=f.read()
    remove(name)
    
    with open(args.output,'w') as f:
        f.write(title+',01'+'\n'+data)
    
    print('Generated',abspath(args.output))
    
