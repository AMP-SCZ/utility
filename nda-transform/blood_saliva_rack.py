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
        return '1903-03-03'

    Y=redcap_date[:4]
    m,d=redcap_date[5:].split('-')
    new_date=f'{m}/{d}/{Y}'

    return new_date


nimh_code={
    'YA' : '914',
    'LA' : '1032',
    'OR' : '1033',
    'BI' : '1034',
    'NL' : '1035',
    'NC' : '1036',
    'SD' : '1042',
    'CA' : '1037',
    'SF' : '1038',
    'PA' : '1039',
    'SI' : '1040',
    'PI' : '1041',
    'NN' : '1043',
    'IR' : '1044',
    'TE' : '1045',
    'GA' : '1046',
    'WU' : '1047',
    'HA' : '1048',
    'MT' : '1049',
    'KC' : '1050',
    'PV' : '1051',
    'MA' : '1052',
    'CM' : '1053',
    'MU' : '1054',
    'SL' : '1055',
    'UR' : '1056',
    'OH' : '1057'
}

matcode_var={
    'WB': 'chrblood_wb1id chrblood_wb1pos chrblood_wb2id chrblood_wb2pos chrblood_wb3id chrblood_wb3pos',
    'EPSE': 'chrblood_se1id chrblood_se1pos chrblood_se2id chrblood_se2pos chrblood_se3id chrblood_se3pos',
    'EPPL': 'chrblood_pl1id chrblood_pl1pos chrblood_pl2id chrblood_pl2pos chrblood_pl3id chrblood_pl3pos '+ \
          'chrblood_pl4id chrblood_pl4pos chrblood_pl5id chrblood_pl5pos chrblood_pl6id chrblood_pl6pos',
    'EPBC': 'chrblood_bc1id chrblood_bc1pos chrblood_bc1box',
    'S': 'chrsaliva_id1a chrsaliva_pos1a chrsaliva_box1a chrsaliva_time1 chrsaliva_id1b chrsaliva_pos1b chrsaliva_box1b chrsaliva_time1 '+ \
         'chrsaliva_id2a chrsaliva_pos2a chrsaliva_box2a chrsaliva_time2 chrsaliva_id2b chrsaliva_pos2b chrsaliva_box2b chrsaliva_time2 '+ \
         'chrsaliva_id3a chrsaliva_pos3a chrsaliva_box3a chrsaliva_time3 chrsaliva_id3b chrsaliva_pos3b chrsaliva_box3b chrsaliva_time3'

}


def populate(i):

    src_subject_id=basename(file).split('.')[0]
    try:
        dfshared.loc[src_subject_id]
    except KeyError:
        return i


    if dfshared.loc[src_subject_id,'phenotype']=='CHR':
        arm=1
        cohort='Proband'
    else:
        arm=2
        cohort='Control'


    # get shared variables
    subjectkey=dfshared.loc[src_subject_id,'subjectkey']
    sex='Male' if dfshared.loc[src_subject_id,'sex']=='M' else 'Female'
    _src_subject_id=nimh_code[src_subject_id[:2]] + '-' + src_subject_id

    chric_consent_date=get_value('chric_consent_date',f'screening_arm_{arm}')


    for matcode in 'WB EPSE EPPL EPBC'.split():
        v1=matcode_var[matcode]
        
        if get_value('chrblood_missing',f'{event}_arm_{arm}')=='1':
            # no data in this form
            continue
            
        draw_date=get_value('chrblood_drawdate',f'{event}_arm_{arm}')
        if len(draw_date)<10:
            continue
        else:
            draw_time=draw_date[11:]
            draw_date=draw_date[:10]

        # calculate age on draw_date
        months=months_since_consent(draw_date,chric_consent_date)
        interview_age=dfshared.loc[src_subject_id,'interview_age']+months
        
        rack_code=get_value('chrblood_rack_barcode',f'{event}_arm_{arm}')
        if matcode=='EPBC':
            rack_code=get_value('chrblood_bc1box',f'{event}_arm_{arm}')

        # deal with people's state of minds
        rack_code=rack_code.strip()
        if rack_code in ['-3','-9']:
            print('Blood rack code',rack_code)
            continue
        
        for j,v in enumerate(v1.split()):
            value=get_value(v,f'{event}_arm_{arm}')
            if j%2==0:
                inventory_code=value
            else:
                pos_on_rack=value
                
                df.loc[i]=[rack_code,pos_on_rack,nda_date(draw_date),inventory_code,'',matcode,'N/A',
                    _src_subject_id,subjectkey,event,cohort,sex,interview_age,'Months','',draw_time]
                i+=1
    


    if get_value('chrsaliva_missing',f'{event}_arm_{arm}')=='1':
        # no data in this form
        return i
    
    # repeat the above for saliva
    for matcode in 'S'.split():
        v1=matcode_var[matcode]
        
        draw_date=get_value('chrsaliva_coldate',f'{event}_arm_{arm}')
        if len(draw_date)<10:
            continue
            
        # calculate age on draw_date
        months=months_since_consent(draw_date,chric_consent_date)
        interview_age=dfshared.loc[src_subject_id,'interview_age']+months
        
        
        for j,v in enumerate(v1.split()):
            value=get_value(v,f'{event}_arm_{arm}')
            if j%4==0:
                inventory_code=value
            elif j%4==1:
                pos_on_rack=value
            elif j%4==2:
                rack_code=value
            elif j%4==3:
                draw_time=value

                # deal with people's state of minds
                rack_code=rack_code.strip()
                if rack_code in ['-3','-9']:
                    print('Saliva rack code',rack_code)
                    continue

                if rack_code[:6].lower()=='pronet':
                    rack_code='ProNET-'+rack_code.strip()[-4:]

                
                df.loc[i]=[rack_code,pos_on_rack,nda_date(draw_date),inventory_code,'',matcode,'N/A',
                    _src_subject_id,subjectkey,event,cohort,sex,interview_age,'Months','',draw_time]
                i+=1


    return i



if __name__=='__main__':

    parser= argparse.ArgumentParser("Make data frame to submit to NDA")
    parser.add_argument("--root", required=True,
        help="/path/to/PHOENIX/GENERAL/")
    parser.add_argument("-o","--output", required=True,
        help="/path/to/submission_ready.csv")
    parser.add_argument("-t","--template", required=True,
        help="*/processed/*/surveys/*.Pronet.json")
    parser.add_argument("-e","--event", required=True,
        help="Event name: screening, baseline, month_1, etc.")
    parser.add_argument("--shared", required=True,
        help="/path/to/ndar_subject01*.csv containing fields shared across NDA dicts")

    
    args= parser.parse_args()
    event=args.event
        
    # load shared ndar_subject01
    with open(args.shared) as f:
        title,df=f.read().split('\n',1)

        _,name=mkstemp()
        with open(name,'w') as fw:
            fw.write(df)
        
        dfshared=pd.read_csv(name)
        remove(name)
        dfshared.set_index('src_subject_id',inplace=True)
    
    
    _columns='Plate #,position,collection date,inventory code,,Matcode,N/A,'+ \
             'subject code,GUID,Visit ID,Pedigree,Genetic Gender,Age,Age Unit,Form ID,collection time'
    df=pd.DataFrame(columns=_columns.split(','))
    i=0


    dir_bak=getcwd()
    chdir(args.root)
    
    files=glob(args.template)

    for row,file in enumerate(files):
        
        print('Processing',file)
        
        with open(file) as f:
            dict1=json.load(f)

        i=populate(i)


    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_colwidth", None)

    chdir(dir_bak)
    
    df.to_csv(args.output,index=False)
    
    print('Generated',abspath(args.output))

