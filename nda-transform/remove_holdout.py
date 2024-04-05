#!/usr/bin/env python
"""
Removes subjects present in holdout.txt from another CSV file

Expects the holdout.txt to have a subject_id in each line:

Sample holdout.txt:

AB12345
CD67890
...

Expects the CSV file to have two header lines and the subject_id as its
second column:

Sample CSV file:

ndar_subject,01
subjectkey,src_subject_id,interview_date,...
val_1,AB12345,val_3
val_4,CD67890,val_6
...

Overwrites the original CSV file with the subjects removed, and backs it up
as <filename>.orig
"""

import argparse
from pathlib import Path
from typing import Set


def get_subjects_to_remove(holdout_list: Path) -> Set[str]:
    """
    Get the subjects to remove from the holdout list
    """
    subjects = set()
    with open(holdout_list, "r") as f:
        for line in f:
            subjects.add(line.strip())

    return subjects


def remove_subjects(holdout_list: Path, target_file: Path):
    """
    Remove subjects from the input CSV file
    """
    subjects_to_remove = get_subjects_to_remove(holdout_list)

    target_file_orig = target_file.with_suffix(target_file.suffix + ".orig")
    target_file.rename(target_file_orig)

    removed_counter = 0
    with open(target_file_orig, "r") as f:
        lines = f.readlines()
        with open(target_file, "w") as t:
            for idx, line in enumerate(lines):
                if idx <= 1:
                    t.write(line)
                    continue

                subject_id = line.split(",")[1]
                if subject_id in subjects_to_remove:
                    removed_counter += 1
                    continue
                t.write(line)

    print(f"Removed {removed_counter} subjects")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Removes subjects from CSV file")
    parser.add_argument(
        "-l", "--holdout", type=str, help="Holdout list file", required=True
    )
    parser.add_argument(
        "-i", "--input", type=str, help="Input CSV file", required=True
    )
    args = parser.parse_args()

    holdout_list = Path(args.holdout)
    target_file = Path(args.input)

    print(f"Removing subjects from: {target_file}")
    print(f"Using holdout list: {holdout_list}")

    remove_subjects(holdout_list, target_file)
