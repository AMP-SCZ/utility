#!/usr/bin/env python
import sys
import pandas as pd
from os.path import abspath, basename

if len(sys.argv)<2 or sys.argv[1] in ['-h','--help']:
    print(f'''Usage: {basename(__file__)} AMPSCZFormRepository_DataDictionary_*.csv''')
    exit(0)

infile= abspath(sys.argv[1])

df= pd.read_csv(infile)
type_groups= df.groupby('Field Type')
checkbox_group= type_groups.get_group('checkbox')

df1= df.copy()
for _,row in checkbox_group.iterrows():
    options= row['Choices, Calculations, OR Slider Labels'].split(' | ')
    for o in options:
        row1= row.copy()
        var= row1['Variable / Field Name']
        num= int(o.split(', ')[0])
        # positive values are joined by three _
        # negative values are joined by four _
        if num>0:
            row1['Variable / Field Name']= f'{var}___{num}'
        else:
            row1['Variable / Field Name']= f'{var}____{abs(num)}'

        df1= df1.append(row1, ignore_index=True)


outfile= infile.split('.csv')[0]+'_checkbox'+'.csv'
df1.to_csv(outfile, index=False)

