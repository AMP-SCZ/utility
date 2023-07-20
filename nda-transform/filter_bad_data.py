#!/usr/bin/env python

import pandas as pd
from shutil import move
from os import getcwd, chdir, remove
from tempfile import mkstemp

dir_bak=getcwd()
chdir('/data/predict1/to_nda/nda-submissions/network_combined/')

dfpro=pd.read_excel('form_status_tracker_PRONET.xlsx')
dfpre=pd.read_excel('form_status_tracker_PRESCIENT.xlsx')


# combine psychs_screening and psychs_followup columns

def combine_psychs(dfp):

    dfp['psychs_screening']=['']*dfp.shape[0]
    dfp['psychs_baseline']=['']*dfp.shape[0]

    # psychs_screening
    for i,row in dfp.iterrows():
        if pd.isna(row['psychs_p1p8_screening']) and pd.isna(row['psychs_p9ac32_screening']):
            dfp.loc[i,'psychs_screening']=None
        else:
            dfp.loc[i,'psychs_screening']='omit'

    # psychs_followup
    for i,row in dfp.iterrows():

        if row['HC or CHR']=='Clinical High Risk':
            condition=pd.isna(row['psychs_p1p8_fu_baseline']) and pd.isna(row['psychs_p9ac32_fu_baseline'])
        else:
            condition=pd.isna(row['psychs_p1p8_fu_hc_baseline']) and pd.isna(row['psychs_p9ac32_fu_hc_baseline'])

        if pd.isna(row['psychs_screening']) and condition:
            dfp.loc[i,'psychs_baseline']=None
        else:
            dfp.loc[i,'psychs_baseline']='omit'

    return dfp


dfpro=combine_psychs(dfpro)
dfpre=combine_psychs(dfpre)


dfmap=pd.read_csv('/data/predict1/utility/nda-transform/tracker_column.csv')
dfmap.set_index('nda_data_file',inplace=True)

subjects=[]

print('\n(computer shape,human shape)\n')
for c in dfmap.index:
 
    column=dfmap.loc[c]['tracker_column']
    
    print(c,column)
            
    _df=pd.concat( (dfpre[['subject','current timepoint',column]], dfpro[['subject','current timepoint',column]]) )
    _df.set_index('subject',inplace=True)
    
    dfdata=pd.read_csv(c,dtype=str,header=1)
    dfdata1=dfdata.copy()
    
    # for each row in dfdata
    #   if there is a value in _df
    #       delete that row from dfdata
    
    for i,row in dfdata.iterrows():
        try:
            cell=_df.loc[ row['src_subject_id'],column ]
        except:
            # if the subject does not exist in tracker, omit it
            cell='omit'
            print(row['src_subject_id'], 'does not exist')
            subjects.append(row['src_subject_id'])

        if not pd.isna(cell) or \
            _df.loc[ row['src_subject_id'],'current timepoint' ]=='removed' \
            or int(row['interview_age'])<10:
            dfdata1.drop(i,inplace=True)
            
            
    _,name=mkstemp()
    dfdata1.to_csv(name,index=False)
    with open(name) as f:
        data=f.read()
    remove(name)

    _c=c.strip('.csv')
    title=_c[:-2]+','+_c[-2:]


    # move(c,f'original/{c}')
    # with open(c,'w') as f:
    with open(f'filtered/{c}','w') as f:
        f.write(title+'\n'+data)

    
    print(dfdata.shape, dfdata1.shape)
    print('')


# print nonexistent subjects
for s in set(subjects):
    print(s)


chdir(dir_bak)

    
