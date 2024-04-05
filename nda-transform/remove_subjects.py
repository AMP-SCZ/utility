#!/usr/bin/env python
"""
Removes subjects from holdout_list file, from another CSV file

Expects holdout_list to be a file withe a subject_id in each
row / line to be removed:

Sample holdout.txt:
AB12345
CD67890
...

Expects the CSV file to dual line headers and the subject_id as its
second column:

Sample CSV file:
col_1,subject_id,col_3
val_1,AB12345,val_3
val_4,CD67890,val_6
...

Overwrites the target CSV file with the subjects removed, and backs up
the original file with a <filename.ext>.orig extension
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

    print(f"Fount {len(subjects)} subjects to remove")
    return subjects


def remove_subjects(holdout_list: Path, target_file: Path):
    """
    Remove subjects from the target CSV file
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
    print(f"Removed subjects from {target_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Removes subjects from CSV file")
    parser.add_argument(
        "-hl", "--holdout_list", type=str, help="Holdout list file", required=True
    )
    parser.add_argument(
        "-tf", "--target_file", type=str, help="Target CSV file", required=True
    )
    args = parser.parse_args()

    holdout_list = Path(args.holdout_list)
    target_file = Path(args.target_file)

    print(f"Removing subjects from {target_file}")
    print(f"Using holdout list: {holdout_list}")

    remove_subjects(holdout_list, target_file)
