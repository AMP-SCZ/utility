#!/usr/bin/env python
"""
Counts unique and duplicate files for NDA submissions
"""

import argparse
from pathlib import Path
from typing import Dict, List, Literal, Optional, Set

import pandas as pd


def count_files(
    project_path: Optional[Path],
    source_path: Path,
    files: List[Path],
    context: Literal["aws", "eris"],
):
    """
    Count unique and duplicate files in the given list of files
    """
    files_count: int = 0
    unique_files: Set = set()
    duplicate_files_count: Dict[str, int] = {}

    file_columns = (
        "data_file1 data_file2 image_file image_manifest bvalfile bvecfile transcript_file".split()
    )

    for file in files:
        print(f"Checking {file}")

        if context == "eris":
            _data_file_path = source_path
            df = pd.read_csv(file, header=1)
        else:
            nda_submissions_path = project_path / "nda-submissions"
            df = pd.read_csv(file)
            _data_file_path = nda_submissions_path / df.loc[0]["SUBMISSION_FOLDER_NAME"]

        # check a file only if at least one file_columns exist
        check_file = False
        for c in file_columns:
            if c in df.columns:
                check_file = True
                break

        if not check_file:
            continue

        for _, row in df.iterrows():
            for c in file_columns:
                if c in df.columns:
                    if not pd.isna(row[c]):
                        data_file = row[c]
                        data_file_path: Path = _data_file_path / data_file

                        if not data_file_path.exists():
                            print(f"File does not exist: {data_file_path}")
                        else:
                            files_count += 1
                            if data_file_path not in unique_files:
                                unique_files.add(data_file_path)
                            else:
                                # count duplicates
                                manifest = file.name
                                if manifest in duplicate_files_count:
                                    duplicate_files_count[manifest] += 1
                                else:
                                    duplicate_files_count[manifest] = 1

    print(f"Total files: {files_count}")
    print(f"Total unique files: {len(unique_files)}")
    print(f"Duplicates: {duplicate_files_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count unique and duplicate files")
    parser.add_argument("-i", "--id", type=str, help="Submission id", default="0")
    parser.add_argument("-c", "--collection", type=str, help="""Collection id:
3705: prod-ampscz, 4366: prod-ampscz-pii, 0: eris
""", choices=["3705", "4366", "0"], default="0"
    )
    args = parser.parse_args()

    submission_id = args.id
    collection_id = args.collection

    print(f"Submission id: {submission_id}")
    print(f"Collection id: {collection_id}")

    if submission_id == "0" or collection_id == "0":
        # ERIS
        CONTEXT = "eris"
        PROJECT_PATH = None
        source_path = Path("/data/predict1/to_nda/nda-submissions/network_combined")
        files = source_path.glob("*csv")
    else:
        # AWS
        CONTEXT = "aws"
        if collection_id == "3705":
            PROJECT_PATH = Path("/volumes/prod-ampscz")
        elif collection_id == "4366":
            PROJECT_PATH = Path("/volumes/prod-ampscz-pii")
        else:
            raise ValueError(f"Unknown collection id: {collection_id}")
        source_path = PROJECT_PATH / "collaboration-space" / collection_id
        files = source_path.glob(f"*/csv/{submission_id}/part-*csv")

    file_paths = list(files)
    file_paths = sorted(file_paths)

    print(f"Context: {CONTEXT}")
    print(f"Source path: {source_path}")
    print(f"Total files: {len(file_paths)}")

    count_files(
        project_path=PROJECT_PATH,
        source_path=source_path,
        files=file_paths,
        context=CONTEXT,
    )
