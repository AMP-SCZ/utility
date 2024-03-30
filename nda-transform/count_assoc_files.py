#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import sys

# Usage:
# at AWS workspace:
# __file__ 65021 3705
# at ERIS cluster:
# __file__ 0 0

nda_submissions_path = Path("/volumes/prod-ampscz/nda-submissions")
id = sys.argv[1]
collection = sys.argv[2]

if id=='0' or collection=='0':
    source_path = Path('/data/predict1/to_nda/nda-submissions/network_combined')
    files = source_path.glob(f'*csv')
else:
    source_path = Path(f"/volumes/prod-ampscz/collaboration-space/{collection}")
    files = source_path.glob(f"*/csv/{id}/part-*csv")

file_columns='data_file1 data_file2 image_file bvalfile bvecfile transcript_file'.split()

count=0
for file in files:
    print("Checking", file)

    
    if id=='0' or collection=='0':
        _data_file_path = source_path
        df = pd.read_csv(file, header=1)
    else:
        df = pd.read_csv(file)
        _data_file_path = nda_submissions_path / df.loc[0]["SUBMISSION_FOLDER_NAME"]


    # check a file only if at least one file_columns exist
    exist=0
    for c in file_columns:
        if c in df.columns:
            exist=1
            break
    if not exist:
        continue


    for idx, row in df.iterrows():
        
        for c in file_columns:
        
            if c in df.columns:
                if not pd.isna(row[c]):
                    data_file = row[c]

                    data_file_path: Path = _data_file_path / data_file

                    if not data_file_path.exists():
                        print(f"File does not exist: {data_file_path}")
                    else:
                        count+=1

print('Total files', count)

