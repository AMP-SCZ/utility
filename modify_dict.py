#!/usr/bin/env python

import sys
import pandas as pd
from os.path import abspath, basename

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {basename(__file__)} AMPSCZFormRepository_DataDictionary_*.csv''')
    exit(0)

infile= abspath(sys.argv[1])
df= pd.read_csv(infile, encoding='ISO-8859-1', dtype=str)

### append ___ or ____ to checkbox variables
type_groups= df.groupby('Field Type')
checkbox_group= type_groups.get_group('checkbox')

df1= df.copy()
for _,row in checkbox_group.iterrows():
    sep=" | "
    if sep not in row['Choices, Calculations, OR Slider Labels']:
        sep="|"
    options= row['Choices, Calculations, OR Slider Labels'].split(sep)
    
    for o in ['-9, Missing', '-3, Not applicable']:
        options.append(o)

    for o in options:
        row1= row.copy()
        var= row1['Variable / Field Name']
        num= int(o.split(', ')[0])
        # positive values are joined by three _
        # negative values are joined by four _
        if num>=0:
            row1['Variable / Field Name']= f'{var}___{num}'
        else:
            row1['Variable / Field Name']= f'{var}____{abs(num)}'

        df1= df1.append(row1, ignore_index=True)
    
    # date variables cannot be converted to integers, deal with them differently
    if row1['Text Validation Type OR Show Slider Number']=='date_ymd':
        for num in ['1909_09_09','1903_03_03','1901_01_01']:
            row1['Variable / Field Name']= f'{var}___{num}'
            df1= df1.append(row1, ignore_index=True)




### remove dateerror variables, calculations, and branching logics
_df2=[]
for i,row in df1.iterrows():
    if row['Field Type']=='descriptive' and 'dateerror' in row['Variable / Field Name']:
        continue
    
    if not pd.isna(row['Branching Logic (Show field only if...)']):
        row['Branching Logic (Show field only if...)']=''
    
    if row['Field Type']=='calc':
        row['Choices, Calculations, OR Slider Labels']=''
        
    _df2.append(row)
    
df2=pd.DataFrame(_df2,columns=df.columns)
df2.to_csv(infile+'.modified',index=False)

