#!/usr/bin/env python

import argparse
import pandas as pd
from shutil import copyfile
from tempfile import mkstemp
from os import remove

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Removes subjects from CSV file")
    parser.add_argument("-r", "--recruit", type=str, help="Recruitment report with an \
        nda_upload_eligible column having values yes/no", required=True)
    parser.add_argument("-i", "--input", type=str, help="Input CSV file", required=True)
    args = parser.parse_args()

    df= pd.read_csv(args.input, dtype=str, header=1)        
    df_eligible= pd.read_csv(args.recruit)
    df_eligible.set_index('subject_id', inplace=True)

    df1= pd.DataFrame(columns=df.columns)
    j=0
    for i,row in df.iterrows():
        s=row['src_subject_id']
        try:
            assert df_eligible.loc[s,'nda_upload_eligible'].lower()=='yes'
            df1.loc[j]=row
            j+=1
        except:
            pass


    _,name=mkstemp()
    df1.to_csv(name,index=False)
        
    with open(name) as f:
        data=f.read()
    remove(name)
    
    title='ndar_subject,01'
    copyfile(args.input, args.input+'.orig')
    with open(args.input,'w') as f:
        f.write(title+'\n'+data)

