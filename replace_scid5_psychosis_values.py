#!/usr/bin/env python

import sys
import pandas as pd
import argparse
from os import chdir, getcwd
from glob import glob

def main():

    parser = argparse.ArgumentParser(description='This script removes incompatible date and number values \
        from RPMS scid5_psychosis_mood_substance_abuse form.')
    parser.add_argument('-s', type=str, required=True, help='AMPSCZ ID for loading ${s}_scid5_psychosis_mood_substance_abuse.csv')
    parser.add_argument('-d', type=str, required=True, help='Directory containing REDCap dictionary')

    args = parser.parse_args()

    dirbak= getcwd()
    chdir(args.d)
    dfdict= pd.read_csv(glob('*_DataDictionary_*')[0])
    chdir(dirbak)

    filename= glob(f'{args.s}_scid5_psychosis_mood_substance_abuse.csv')[0]
    df= pd.read_csv(filename,dtype=str)

    for i,row in dfdict.iterrows():
        if row['Form Name']=='scid5_psychosis_mood_substance_abuse':

            var= row['Variable / Field Name']
            values= df[var].values

            # check for comptabile values
            if row['Text Validation Type OR Show Slider Number'] == 'date_ymd':
                for j,val in enumerate(values):
                    # a date value is 10 characters with two /
                    if len(val)!=10 and re.findall('/',val)!=2:
                        values[j]= ''

            elif row['Text Validation Type OR Show Slider Number'] == 'number':
                for j,val in enumerate(values):
                    try:
                        values[j]= int(val)
                    except:
                        try:
                            values[j]= float(val)
                        except:
                            values[j]= ''
                    
            elif row['Text Validation Type OR Show Slider Number'] == 'integer':
                for j,val in enumerate(values):
                    try:
                        values[j]= int(val)
                    except:
                        values[j]= ''


        df[var]= values



    df.to_csv(filename, index=False)


if __name__ == '__main__':
    main()





