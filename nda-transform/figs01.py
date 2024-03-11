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

fam_dict={
    'mother':1,
    'father':2,
    'sibling1':3,
    'sibling2':4,
    'sibling3':5,
    'sibling4':6,
    'sibling5':7,
    'sibling6':8,
    'sibling7':9,
    'sibling8':10,
    'sibling9':11,
    'child1':12,
    'child2':13,
    'child3':14,
    'child4':15
}


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
    
    dict1={}
    # get shared variables
    dict1['src_subject_id']=src_subject_id
    for v in ['subjectkey','sex']:
        dict1[v]=dfshared.loc[src_subject_id,v]


    # get form specific variables
    dict1['interview_date']=nda_date(interview_date)
    
    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')
    months=months_since_consent(interview_date,chric_consent_date)
    dict1['interview_age']=dfshared.loc[src_subject_id,'interview_age']+months
    
    missing=get_value(f'{prefix}_missing',f'{event}_arm_{arm}')
    if missing=='':
        # not clicked
        missing='0'
    dict1['ampscz_missing']=missing
    if missing=='1':
        dict1['ampscz_missing_spec']=get_value(f'{prefix}_missing_spec',f'{event}_arm_{arm}')[1]
    else:
        dict1['ampscz_missing_spec']=''

    
    for member in fam_dict.keys():
        dict2={}
        dict2['chrfigs_fam']=fam_dict[member]

        for v in columns:
            
            if prefix in v and v!='chrfigs_fam':
                v1=v.replace('fam',member)
                value=get_value(v1,f'{event}_arm_{arm}')
                
                vrange=definition.loc[v,'ValueRange']
                if not pd.isna(vrange):
                    if '-300' in vrange or '-900' in vrange:
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
                        value=value[:int(size)]

                elif definition.loc[v,'DataType']=='Date':
                    value=nda_date(value)

                elif definition.loc[v,'DataType']=='Float':
                    try:
                        value=round(float(value),3)
                    except ValueError:
                        pass

                dict2[v]=value


        _row={**dict1,**dict2}

        rows.append(_row)


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
    parser.add_argument("-e","--event", required=True,
        help="Event name: screening, baseline, month_1, etc.")
    parser.add_argument("-p","--prefix", required=True,
        help="Variable name prefix e.g. chrnsipr, chrpgis, chrassist, etc.")
    parser.add_argument("--member",
        help="Family member: father, mother, sibling, children. It replaces fam string in chrfigs_fam_* variables")
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

    columns=['subjectkey','src_subject_id','interview_date','interview_age','sex']
    for c in definition.index:
        if prefix in c:
            columns.append(c.strip())

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
    
    rows=[]
    files=glob(args.template)
    for row,file in enumerate(files):
        
        print('Processing',file)
        
        with open(file) as f:
            dict1=json.load(f)

        populate()

    df=pd.DataFrame(rows,columns=columns)
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
    
