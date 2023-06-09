#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob
from os.path import basename,abspath
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
    try:
        age= datetime.strptime(interview,'%Y-%m-%d')-datetime.strptime(consent,'%Y-%m-%d')
    except ValueError:
        age= datetime.strptime(interview,'%m/%d/%Y')-datetime.strptime(consent,'%Y-%m-%d')

    return round(age.days/30)


def nda_date(redcap_date):
    if redcap_date=='':
        # REDCap missing: 1909-09-09
        # REDCap N/A: 1903-03-03
        return '03/03/1903'

    # check if it is already in NDA format
    try:
        datetime.strptime(redcap_date,'%m/%d/%Y')
        return redcap_date
    except ValueError:
        pass

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

    try:
        interview_date=data.loc[src_subject_id,interview_date_var]
    except KeyError:
        # no data for this subject
        return


    # extract the src_subject_id group
    group=data.loc[src_subject_id]
    
    subjectkey=dfshared.loc[src_subject_id,'subjectkey']
    sex=dfshared.loc[src_subject_id,'sex']
    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')

    # populate one row in df for each row in group
    current_index=df.shape[0]

    # Pandas throw a warning if df is appended by src_subject_id
    # df should be appended by numeric index anyway, so resetting its index
    group.reset_index(inplace=True)
    for i,r in group.iterrows():

        interview_date=r['interview_date']
        months=months_since_consent(interview_date,chric_consent_date)
        r['interview_age']=dfshared.loc[src_subject_id,'interview_age']+months
        r['subjectkey']=subjectkey
        r['sex']=sex

        df.loc[current_index+i]=r



if __name__=='__main__':

    parser= argparse.ArgumentParser("Make data frame to submit to NDA")
    parser.add_argument("--dict", required=True,
        help="NDA short name of the data structure e.g. actirec01, image03")
    parser.add_argument("--root", required=True,
        help="/path/to/PHOENIX/GENERAL/")
    parser.add_argument("-t","--template", required=True,
        help="*/processed/*/surveys/*.Pronet.json")
    parser.add_argument("-o","--output", required=True,
        help="/path/to/submission_ready.csv")
    parser.add_argument("--data", required=True,
        help="/path/to/data01*.csv containing non-survey data e.g. actirec01, image03")
    parser.add_argument("--interview_date_var",
        help="Provide interview date variable if it is not interview_date in --data file")
    parser.add_argument("--shared", required=True,
        help="/path/to/ndar_subject01*.csv containing fields shared across NDA dicts")
    parser.add_argument("--version",
        help="version string in form's NDA short name: 01, 03, etc.")

    
    args= parser.parse_args()
    
    # load shared ndar_subject01
    with open(args.shared) as f:
        _,df=f.read().split('\n',1)

        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(df)
        
        dfshared=pd.read_csv(name)
        remove(name)
        dfshared.set_index('src_subject_id',inplace=True)
    
    columns=['subjectkey','src_subject_id','interview_date','interview_age','sex']

    data=pd.read_csv(args.data)
    df=pd.DataFrame(columns=data.columns)
    data.set_index('src_subject_id',inplace=True)

    if args.interview_date_var:
        interview_date_var=args.interview_date_var
    else:
        interview_date_var='interview_date'

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
    
    version=args.version
    title=re.search(f'/(.+?){version}_template.csv',args.dict).group(1)
    with open(args.output,'w') as f:
        f.write(f'{title},{version}\n'+data)
    
    print('Generated',abspath(args.output))
    
