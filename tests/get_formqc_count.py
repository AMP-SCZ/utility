#!/usr/bin/env python

import pandas as pd
from glob import glob


def get_count():

    for file in files:
        df=pd.read_csv(file)

        if len(df[var].values)>1:
            print(file,'has multiple rows!')
            
        elif len(df[var].values)==0:
            print(file, 'does not have any row!')

        else:
            if pd.isna(df[var].values[0]):
                count['']+=1
            else:
                key=int(df[var].values[0])
                count[key]+=1

    print(count,end='')
    print(' Total:',sum(count.values()))
    print('')


if __name__=='__main__':
    
    var='chrcrit_part'
    files=glob('/data/predict1/data_from_nda/formqc/*_inclusionexclusion_criteria_review*.csv')
    count={1:0, 2:0, '':0}
    print(var,'count:')
    get_count()


    var='included_excluded'
    count={1:0, 0:0, '':0}
    print(var,'count:')
    get_count()


    var='chrdemo_sexassigned'
    count={1:0, 2:0, '':0}
    files=glob('/data/predict1/data_from_nda/formqc/*_sociodemographics*.csv')
    print(var,'count:')
    get_count()


    var='visit_status'
    count={0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 98:0, 99:0, '':0}
    files=glob('/data/predict1/data_from_nda/formqc/*_informed_consent_run_sheet*.csv')
    print(var,'count:')
    get_count()