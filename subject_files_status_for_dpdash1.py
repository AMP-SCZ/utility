#!/bin/bash

import json
from glob import glob
from os.path import abspath, basename, dirname, join as pjoin
import pandas as pd
import sys


def get_mri_status():
    """available variables:
    nda_root
    network
    timepoint
    s: JSON path
    data: two-element JSON array of timepoint of CHR and HC arms
    """
    pass

    # return a dictionary of {MRI QC Score, Data Transferred, Protocol Followed, Acquisition Date}


def get_eeg_status():
    pass

    
def get_avl_status():
    pass



if __name__=='__main__':

    nda_root='/data/predict1/data_from_nda/'
    network='Pronet'
    timepoint='baseline'

    outdir=pjoin(nda_root,f'{network}_status')

    surveys=glob(pjoin(nda_root,network,f'PHOENIX/PROTECTED/{network}??/raw/*/surveys/*.{network}.json'))


    # initiate DataFrame
    df1=pd.DataFrame(columns=['day,reftime,timeofday,weekday,subject_id,site'.split(',')])

    for s in surveys:

        with open(s) as f:
            data1=json.load(f.read())


        # extract and join CHR and HC arms
        data=[]
        for d in data:
            if timepoint in d['redcap_event_name']:
                data.append(d)


        subject=basename(s).split('.')[0]
        site=subject[:2]

        # initialize dict
        dict_all={'day':1,'reftime':'','timeofday':'','weekday':'',
            'site':site,'subject_id':subject}

        
        # populate MRI block
        dict_mri=get_mri_status()
            
        # populate EEG block
        dict_eeg=get_eeg_status()

        # populate A/V/L block
        dict_avl=get_avl_status()


        # join the dicts
        dict_all.update(dict_mri)
        dict_all.update(dict_eeg)
        dict_all.update(dict_avl)

        # transform to DataFrame
        df=pd.DataFrame(dict_all)

        # write out subject DataFrame
        outfile=pjoin(outdir,f'{site}-{subject}-data_{timepoint}.day1to1.csv')
        df.to_csv(outfile,index=False)
    
    
