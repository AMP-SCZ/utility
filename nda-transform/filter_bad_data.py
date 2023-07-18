#!/usr/bin/env python

import pandas as pd
from shutil import move,copyfile
from os import getcwd, chdir

dir_bak=getcwd()
chdir('/data/predict1/to_nda/nda-submissions/network_combined/')

dfpro=pd.read_excel('form_status_tracker_PRONET.xlsx')
dfpre=pd.read_excel('form_status_tracker_PRESCIENT.xlsx')

dfmap=pd.read_csv('/data/predict1/utility/nda-transform/tracker_column.csv')
dfmap.set_index('nda_data_file',inplace=True)

subjects=[]
for c in dfmap.index:

    if c.startswith('ampscz_psychs01'):
        continue
        
    column=dfmap.loc[c]['tracker_column']
    
    print(c,column)
            
    _df=pd.concat( (dfpre[['subject',column]], dfpro[['subject',column]]) )
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
            cell=''
            pass
            print(row['src_subject_id'])
            subjects.append(row['src_subject_id'])

        if not pd.isna(cell):
            dfdata1.drop(i,inplace=True)
            
            
    # move(c,c+'.bak')
    # dfdata1.to_csv(f,index=False)
    dfdata1.to_csv(f'filtered/{c}',index=False)
    print(dfdata.shape, dfdata1.shape)
    print('')


for s in set(subjects):
    print(s)

chdir(dir_bak)
    
