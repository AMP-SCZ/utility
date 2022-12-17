#!/usr/bin/env python

from os.path import join as pjoin, dirname
import sys
from glob import glob
import pandas as pd
import numpy as np

def concat_site_csv(data_root,output_root,center_name):

    if len(center_name)==2:
        # site level combination
        template="processed/*/interviews/*/*_combinedQCRecords.csv"
    else:
        # network level combination
        template="PHOENIX/GENERAL/*/processed/*/interviews/*/*_combinedQCRecords.csv"
        
    individual_qc_paths = glob(f"{data_root}/{template}")
    if not individual_qc_paths:
        return
    
    individual_qc_dfs = [pd.read_csv(x) for x in individual_qc_paths]
    individual_qc_concat = pd.concat(individual_qc_dfs)
    individual_qc_concat.reset_index(drop=True, inplace=True)
    individual_qc_concat.rename(columns={"day":"true_day_num"},inplace=True)
    # so it will display in order of patient ID and within ID the day number
    # if different order is wanted, it needs to change
    individual_qc_concat.sort_values(by="true_day_num",inplace=True)
    individual_qc_concat.sort_values(by="patient",kind="stable",inplace=True)
    dpdash_cols = ["day","reftime","timeofday","weekday"]
    dpdash_cols.extend(individual_qc_concat.columns)
    individual_qc_concat["day"] = [x+1 for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat["reftime"] = [np.nan for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat["timeofday"] = [np.nan for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat["weekday"] = [np.nan for x in range(individual_qc_concat.shape[0])]
    individual_qc_concat = individual_qc_concat[dpdash_cols]
    
    individual_qc_concat.to_csv(f"{output_root}/combined-{center_name}-avlqc-day1to1.csv", index=False)
    

if __name__ == '__main__':

    concat_site_csv(f'{sys.argv[1]}/Pronet', f'{sys.argv[1]}/AVL_quick_qc', 'PRONET')
    for site in glob(f'{sys.argv[1]}/Pronet/PHOENIX/GENERAL/*'):
        concat_site_csv(site, f'{sys.argv[1]}/AVL_quick_qc', site[-2:])
    
    concat_site_csv(f'{sys.argv[1]}/Prescient', f'{sys.argv[1]}/AVL_quick_qc', 'PRESCIENT')
    for site in glob(f'{sys.argv[1]}/Prescient/PHOENIX/GENERAL/*'):
        concat_site_csv(site, f'{sys.argv[1]}/AVL_quick_qc', site[-2:])

    
