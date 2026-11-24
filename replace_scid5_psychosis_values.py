#!/usr/bin/env python

import sys
import pandas as pd
import argparse
from os import chdir, getcwd
from glob import glob
import re

def main():

    parser = argparse.ArgumentParser(description='This script removes incompatible date and number values \
        from RPMS scid5_psychosis_mood_substance_abuse form.')
    parser.add_argument('-i', type=str, required=True, help='The scid5_psychosis_mood_substance_abuse.csv file')
    parser.add_argument('-d', type=str, required=True, help='Directory containing REDCap dictionary')

    args = parser.parse_args()

    dirbak= getcwd()
    chdir(args.d)
    dfdict= pd.read_csv(glob('*_DataDictionary_*')[0])
    chdir(dirbak)

    filename= args.i
    df= pd.read_csv(filename,dtype=str, keep_default_na=False)
    df1= df.copy()

    columns= list(df.columns)
    columns.remove('chrscid_interview_date')

    WRITE=False
    for i,row in dfdict.iterrows():
        if row['Form Name']=='scid5_psychosis_mood_substance_abuse':

            MODIFIED= False
            var= row['Variable / Field Name']

            if var not in columns:
                continue

            values= df[var].values

            # check for comptabile values
            if row['Text Validation Type OR Show Slider Number'] == 'date_ymd':
                for j,val in enumerate(values):
                    if pd.isna(val):
                        continue

                    # a date value is 10 characters with two /
                    if len(val)!=10 and re.findall('/',val)!=2:
                        values[j]= ''
                        MODIFIED= True

            elif row['Text Validation Type OR Show Slider Number'] == 'number':
                for j,val in enumerate(values):
                    if pd.isna(val):
                        continue
                    
                    try:
                        values[j]= int(val)
                    except:
                        try:
                            values[j]= float(val)
                        except:
                            values[j]= ''
                            MODIFIED= True
                    
            elif row['Text Validation Type OR Show Slider Number'] == 'integer':
                for j,val in enumerate(values):
                    if pd.isna(val):
                        continue
                    
                    try:
                        values[j]= int(val)
                    except:
                        values[j]= ''
                        MODIFIED= True

            if MODIFIED:
                WRITE=True
                df1[var]= values


    if WRITE:
        df1.to_csv(filename, index=False)


if __name__ == '__main__':
    main()


