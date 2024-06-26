#!/usr/bin/env python

import sys
import pandas as pd
from os.path import abspath, basename

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {basename(__file__)} AMPSCZFormRepository_DataDictionary_*.csv''')
    exit(0)

infile= abspath(sys.argv[1])
df= pd.read_csv(infile, encoding='ISO-8859-1', dtype=str)

if 'field_type' in df.columns:
    FIELD_TYPE='field_type'
    FIELD_NAME='field_name'
    CHOICE_CALC='select_choices_or_calculations'
    BRANCHING='branching_logic'
    VALIDATION='text_validation_type_or_show_slider_number'

elif 'Field Type' in df.columns:
    FIELD_TYPE='Field Type'
    FIELD_NAME='Variable / Field Name'
    CHOICE_CALC='Choices, Calculations, OR Slider Labels'
    BRANCHING='Branching Logic (Show field only if...)'
    VALIDATION='Text Validation Type OR Show Slider Number'


### remove dateerror variables, calculations, and branching logics
_df=[]
for i,row in df.iterrows():
    if row[FIELD_TYPE]=='descriptive' and 'dateerror' in row[FIELD_NAME]:
        continue
    
    if not pd.isna(row[BRANCHING]):
        row[BRANCHING]=''
    
    if row[FIELD_TYPE]=='calc':
        row[CHOICE_CALC]=''
        row[FIELD_TYPE]='text'
        
    _df.append(row)
    
df1=pd.DataFrame(_df,columns=df.columns)

outfile= infile.replace('.csv','_calc_logic.csv')
df1.to_csv(outfile,index=False)



### append ___ or ____ to checkbox variables
type_groups= df1.groupby(FIELD_TYPE)
checkbox_group= type_groups.get_group('checkbox')

df2= df1.copy()
for _,row in checkbox_group.iterrows():
    sep=" | "
    if sep not in row[CHOICE_CALC]:
        sep="|"
    options= row[CHOICE_CALC].split(sep)
    
    for o in ['-9, Missing', '-3, Not applicable']:
        options.append(o)

    for o in options:
        row1= row.copy()
        var= row1[FIELD_NAME]
        num= int(o.split(', ')[0])
        # positive values are joined by three _
        # negative values are joined by four _
        if num>=0:
            row1[FIELD_NAME]= f'{var}___{num}'
        else:
            row1[FIELD_NAME]= f'{var}____{abs(num)}'

        df2= pd.concat((df2,pd.DataFrame([row1])), ignore_index=True)
    
    # date variables cannot be converted to integers, deal with them differently
    if row1[VALIDATION]=='date_ymd':
        for num in ['1909_09_09','1903_03_03','1901_01_01']:
            row1[FIELD_NAME]= f'{var}___{num}'
            df2= pd.concat((df2,pd.dataFrame([row1])), ignore_index=True)

outfile= infile.replace('.csv','_calc_logic_checkbox.csv')
df2.to_csv(outfile,index=False)


