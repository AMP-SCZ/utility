#!/usr/bin/env python

from os.path import join as pjoin
import sys
from glob import glob
import pandas as pd
import numpy as np

def concat_site_csv(data_root="/data/predict/data_from_nda",
    output_root="/data/predict/data_from_nda/AVL_quick_qc",
    center_name="Pronet"):

    individual_qc_paths = glob(
        f"{data_root}/{center_name}/PHOENIX/GENERAL/*/processed/*/interviews/*/*_combinedQCRecords.csv")
    
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
    
    individual_qc_concat.to_csv(pjoin(output_root,"combined-" + center_name + "-avlqc-day1to1.csv"), index=False)
    

if __name__ == '__main__':
    # map command line arguments to function arguments.
    try:
        # sys.argv[1:]= [data_root, output_root, center_name]
        concat_site_csv(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        concat_site_csv()
        
