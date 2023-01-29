#!/usr/bin/env python

from datetime import datetime
import sys
import argparse
from os import remove,getcwd,chdir
import json
from tempfile import mkstemp
import pandas as pd
from glob import glob
from os.path import basename


# this function should have knowledge of dict1
def get_value(var,event):

    for d in dict1:
        if d['redcap_event_name']==event:
            try:
                return d[var]
            except KeyError:
                return ''


def calc_age(consent,interview):
    age= datetime.strptime(consent,'%Y-%m-%d')-datetime.strptime(interview,'%Y-%m-%d')
    return round(age.days/30)


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

    # get form specific variables

    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')
    interview_date=get_value('chrrecruit_interview_date',f'screening_arm_{arm}')
    interview_age=calc_age(chric_consent_date,interview_date)

    for v in ['subjectkey','sex']:
        df.at[row,v]=dfshared.loc[src_subject_id,v]

    for v in ['src_subject_id','interview_date','interview_age']:
        df.at[row,v]=eval(v)
    #df.at[row,'interview_date']=interview_date
    #df.at[row,'interview_age']=interview_age
    
    for v in columns:
        if 'chrrecruit' in v:
            df.at[row,v]=get_value(v,f'screening_arm_{arm}')

    # return df


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
        
        # rename vars
        # df=df.replace('interview_date','chrrecruit_interview_date')
        df=df.replace('ampscz','chrrecruit')

        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(df)
        
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
        f.write(title+'\n'+data)
    

