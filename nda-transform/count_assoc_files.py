from pathlib import Path
import pandas as pd

source_path = Path("/volumes/prod-ampscz/collaboration-space/3705")
nda_submissions_path = Path("/volumes/prod-ampscz/nda-submissions")
id = 59959

files = source_path.glob(f"*/csv/{id}/part-*csv")

for file in files:
    df = pd.read_csv(file)
    if "data_file1" in df.columns:

        for idx, row in df.iterrows():
            data_file = row["data_file1"]
            submission_folder = row["SUBMISSION_FOLDER_NAME"]

            data_file_path: Path = nda_submissions_path / submission_folder / data_file 

            if not data_file_path.exists():
                print(f"File does not exist: {data_file_path}")
                break
