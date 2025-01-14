#!/usr/bin/env python
"""
Removes subjects present in holdout.txt from input CSV file

Expects the holdout.txt to have a subject_id in each line:

AB12345
CD67890
...

===

Or, includes CHR subjects assigned as `in` in inclusion.csv, together with all HC subjects.

Sample inclusion.csv:

ID,sips_pos_tot,assignment
AB12345,7,in
CD67890,17,out
...

Expects the CSV file to have two header lines and the subject_id as its
second column:

ndar_subject,01
subjectkey,src_subject_id,interview_date,...,phenotype,...
val_1,AB12345,val_3,...,CHR,...
val_4,CD67890,val_6,...,HC,...
...

Overwrites the original CSV file after removing the holdout subjects, and backs it up
as <filename>.orig
"""

import argparse
from pathlib import Path
from typing import Set

import pandas as pd


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


def get_subjects_to_include(include_list: Path, input_file: Path) -> Set[str]:
    """
    Get the subjects to include from the include CSV file, together with all HC phenotype
    subjects
    """
    subjects = set()
    ndar_df = pd.read_csv(input_file, skiprows=1)
    inclusion_df = pd.read_csv(include_list)

    hc_subjects = ndar_df[ndar_df["phenotype"] == "HC"][
        "src_subject_id"
    ].values.tolist()
    inclusion_df = inclusion_df[inclusion_df["assignment"] == "in"][
        "ID"
    ].values.tolist()

    subjects.update(hc_subjects)
    subjects.update(inclusion_df)

    return subjects


def include_subjects(include_list: Path, target_file: Path):
    """
    Include subjects from the include_list CSV file
    """
    subjects_to_include = get_subjects_to_include(include_list, target_file)

    target_file_orig = target_file.with_suffix(target_file.suffix + ".orig")
    target_file.rename(target_file_orig)

    included_counter = 0
    removed_counter = 0
    with open(target_file_orig, "r") as f:
        lines = f.readlines()
        with open(target_file, "w") as t:
            for idx, line in enumerate(lines):
                if idx <= 1:
                    t.write(line)
                    continue

                subject_id = line.split(",")[1]
                if subject_id in subjects_to_include:
                    included_counter += 1
                    t.write(line)
                else:
                    removed_counter += 1

    print(f"Included {included_counter} subjects")
    print(f"Removed {removed_counter} subjects")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Removes subjects from CSV file")
    parser.add_argument("-l", "--holdout", type=str, help="Holdout list file")
    parser.add_argument("-c", "--include", type=str, help="Inclusion file with an \
        assignment column having values in/out")
    parser.add_argument("-i", "--input", type=str, help="Input CSV file", required=True)
    args = parser.parse_args()

    # Either holdout or include must be provided
    if not args.holdout and not args.include:
        parser.error("Either holdout or include must be provided")

    if args.holdout and args.include:
        parser.error("Only one of holdout or include must be provided")

    if args.holdout:
        holdout_list = Path(args.holdout)
        target_file = Path(args.input)

        print(f"Removing subjects from: {target_file}")
        print(f"Using holdout list: {holdout_list}")

        remove_subjects(holdout_list, target_file)
    if args.include:
        include_list = Path(args.include)
        target_file = Path(args.input)

        print(f"Including subjects from: {include_list}")

        include_subjects(include_list, target_file)
