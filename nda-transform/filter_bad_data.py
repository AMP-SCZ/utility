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
    
    # introduce a column for rawdata
    # dfp['rawdata']=[None]*dfp.shape[0]

    dfp['psychs_screening']=['']*dfp.shape[0]
    dfp['psychs_baseline']=['']*dfp.shape[0]
    dfp['psychs_month_1']=['']*dfp.shape[0]
    dfp['psychs_month_2']=['']*dfp.shape[0]


    for i,row in dfp.iterrows():

        # psychs_screening
        if pd.isna(row['psychs_p1p8_screening']) and pd.isna(row['psychs_p9ac32_screening']):
            dfp.loc[i,'psychs_screening']=None
        else:
            dfp.loc[i,'psychs_screening']='omit'

        
        if row['cohort']=='CHR':
            FU='_fu_'
        elif row['cohort']=='HC':
            FU='_fu_hc_'
        else:
            dfp.loc[i,'psychs_baseline']='omit'
            dfp.loc[i,'psychs_month_1']='omit'
            dfp.loc[i,'psychs_month_2']='omit'
            continue
        
        # psychs_baseline
        condition=pd.isna(row[f'psychs_p1p8{FU}baseline']) and pd.isna(row[f'psychs_p9ac32{FU}baseline'])
        if pd.isna(row['psychs_screening']) and condition:
            dfp.loc[i,'psychs_baseline']=None
        else:
            dfp.loc[i,'psychs_baseline']='omit'


        if row['cohort']=='CHR':
            
            # psychs_month_1
            condition=pd.isna(row[f'psychs_p1p8{FU}month_1']) and pd.isna(row[f'psychs_p9ac32{FU}month_1'])
            if pd.isna(row['psychs_baseline']) and condition:
                dfp.loc[i,'psychs_month_1']=None
            else:
                dfp.loc[i,'psychs_month_1']='omit'
            
            # psychs_month_2
            condition=pd.isna(row[f'psychs_p1p8{FU}month_2']) and pd.isna(row[f'psychs_p9ac32{FU}month_2'])
            if pd.isna(row['psychs_month_1']) and condition:
                dfp.loc[i,'psychs_month_2']=None
            else:
                dfp.loc[i,'psychs_month_2']='omit'



        elif row['cohort']=='HC':
            
            # psychs_month_2
            condition=pd.isna(row[f'psychs_p1p8{FU}month_2']) and pd.isna(row[f'psychs_p9ac32{FU}month_2'])
            if pd.isna(row['psychs_baseline']) and condition:
                dfp.loc[i,'psychs_month_2']=None
            else:
                dfp.loc[i,'psychs_month_2']='omit'


    return dfp


dfpro=combine_psychs(dfpro)
dfpre=combine_psychs(dfpre)
_df=pd.concat((dfpro,dfpre))
_df.set_index('subject',inplace=True)


dfmap=pd.read_csv('/data/predict1/utility/nda-transform/tracker_column.csv')
dfmap.set_index('nda_data_file',inplace=True)

subjects=[]

print('\n(computer shape,human shape)\n')
for c in dfmap.index:
 
    column=dfmap.loc[c]['tracker_column']
    
    print(c,column)
    
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

        if not pd.isna(cell):
            dfdata1.drop(i,inplace=True)

    print(dfdata.shape[0], dfdata1.shape[0])
    print('')

    # activate this continue to not save anything
    # continue

    _,name=mkstemp()
    dfdata1.to_csv(name,index=False)
    with open(name) as f:
        data=f.read()
    remove(name)


    parts=c.split('01')
    version='01'
    if len(parts)<2:
        parts=c.split('03')
        version='03'
    title=parts[0]+','+version
    print(title)


    move(c,f'original/{c}')
    with open(c,'w') as f:
        f.write(title+'\n'+data)

    

# print nonexistent subjects
for s in set(subjects):
    print(s)


chdir(dir_bak)

    
