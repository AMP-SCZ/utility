#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import sys

nda_submissions_path = Path("/volumes/prod-ampscz/nda-submissions")
id = sys.argv[1]
collection = sys.argv[2]

source_path = Path(f"/volumes/prod-ampscz/collaboration-space/{collection}")

files = source_path.glob(f"*/csv/{id}/part-*csv")

file_columns='data_file1 data_file2 image_file bvalfile bvecfile'.split()

count=0
for file in files:
    print("Checking", file)

    df = pd.read_csv(file)
    
    submission_folder = df.loc[0]["SUBMISSION_FOLDER_NAME"]


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

                    data_file_path: Path = nda_submissions_path / submission_folder / data_file

                    if not data_file_path.exists():
                        print(f"File does not exist: {data_file_path}")
                    else:
                        count+=1

print('Total files', count)

