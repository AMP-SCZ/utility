#!/usr/bin/env python
"""
Filters ndar_subject01 based on the following selection criteria:

NDA Release 3:
1. The participant has to be either CHR or HC
2. If we upload only included subjects, subjects have to fulfill inclusion criteria
3. Additionally, the inclusion form has no QC issues
4. If the participant is a CHR,
    the participant has to fulfill the criteria for the SIPS and/or CAARMS group.
5. If the participant is a HC,
    the participant does not fulfill criteria ofany of the SIPS and CAARMS group.
6. Additionally, the screening PSYCHS forms have no QC issues

5 and 6 can be simplified to:
    Inconsistecy between the SIPS/CAARMS group and the participant's cohort
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

logger = logging.getLogger(__name__)
logargs = {
    "level": logging.DEBUG,
    # "format": "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s",
    "format": "%(asctime)s - %(process)d - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - "
    "%(message)s",
}
logging.basicConfig(**logargs)

DEST_CSV_PATH = "/data/predict1/home/dm1447/data/nda/ndar_subject01_selected_v2.csv"


def get_ndar_subject01_df() -> pd.DataFrame:
    """
    Concatenates all ndar_subject01 files into a single DataFrame

    Looks for all ndar_subject01 files in /data/predict1/to_nda/nda-submissions/ndar_subject01*.csv

    Returns:
        pd.DataFrame: DataFrame containing all ndar_subject01 data
    """
    ndar_csvs = list(
        Path("/data/predict1/to_nda/nda-submissions").glob("ndar_subject01*.csv")
    )
    logger.info(f"Reading ndar_subject01 files: {ndar_csvs}")

    ndar_df = pd.DataFrame()

    for ndar_csv in ndar_csvs:
        # Reak skipping the first row
        temp_df = pd.read_csv(ndar_csv, skiprows=1)
        ndar_df = pd.concat([ndar_df, temp_df])

    ndar_df.reset_index(drop=True, inplace=True)

    return ndar_df


def get_qc_tracker() -> pd.DataFrame:
    """
    Returs QC tracker DataFrame.

    Looks for the following tracker files:
    - /data/predict1/data_from_nda/form_status/form_status_tracker_PRESCIENT.xlsx
    - /data/predict1/data_from_nda/form_status/form_status_tracker_PRONET.xlsx

    Returns:
        pd.DataFrame: DataFrame containing all tracker data
    """
    tracker_files = [
        "/data/predict1/data_from_nda/form_status/form_status_tracker_PRESCIENT.xlsx",
        "/data/predict1/data_from_nda/form_status/form_status_tracker_PRONET.xlsx",
    ]

    logger.info(f"Reading tracker files: {tracker_files}")
    tracker_prescient = pd.read_excel(tracker_files[0])
    tracker_pronet = pd.read_excel(tracker_files[1])
    tracker_df = pd.concat([tracker_prescient, tracker_pronet])

    tracker_df.reset_index(drop=True, inplace=True)

    return tracker_df


def get_variable_value(
    json_file: Path, redcap_event_name: str, redcap_variable_name: str
) -> Optional[str]:
    """
    Returns the value of a redcap_variable_name in a json_file for a specific redcap_event_name

    Args:
        json_file (Path): JSON file containing redcap data
        redcap_event_name (str): Event name to filter
        redcap_variable_name (str): Variable name to return

    Returns:
        Optional[str]: Value of redcap_variable_name for redcap_event_name, if found.
            None otherwise
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data: List[Dict[str, Any]] = json.load(f)

    for event_data in data:
        event_name = event_data["redcap_event_name"]
        if redcap_event_name in event_name:
            redcap_value = event_data.get(redcap_variable_name, None)
            return redcap_value

    return None


def fix_ndar_csv(ndar_like_csv: Path):
    """
    Adds the first row from the original ndar_subject01 csv to the new ndar_like_csv

    Args:
        ndar_like_csv (Path): Path to the new ndar_like_csv

    Returns:
        None
    """
    ndar_csvs = list(
        Path("/data/predict1/to_nda/nda-submissions").glob("ndar_subject01*.csv")
    )
    # Add first row from original ndar_csv
    ndar_csv = ndar_csvs[0]
    with open(ndar_csv, "r", encoding="utf-8") as f:
        first_line = f.readline()

    with open(ndar_like_csv, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(ndar_like_csv, "w", encoding="utf-8") as f:
        f.write(first_line)
        f.writelines(lines)


def select_subjects() -> Tuple[List[str], List[Dict[str, Any]], pd.DataFrame]:
    """
    Filters subjects based on selection criteria.

    Returns:
        Tuple[List[str], List[Dict[str, Any]], pd.DataFrame]: Tuple containing:
            - List of selected subjects
            - List of skipped subjects
            - DataFrame containing selected subjects
    """
    ndar_df = get_ndar_subject01_df()
    qc_tracker_df = get_qc_tracker()

    data_root = Path("/data/predict1/data_from_nda")
    subject_jsons_pattern = "Pr*/PHOENIX/PROTECTED/Pr*/raw/*/surveys/*.Pr*.json"
    logger.info(f"Reading JSON data from {data_root}/{subject_jsons_pattern}")
    subject_jsons = list(data_root.glob(subject_jsons_pattern))
    logger.info(f"Found {len(subject_jsons)} subject jsons")

    selected_subjects: List[str] = []
    skipped_subjects: List[Dict[str, Any]] = []

    new_ndar_df = pd.DataFrame()

    logger.info("Filtering subjects...")
    for idx, row in ndar_df.iterrows():
        subject_id = row["src_subject_id"]

        if idx % (len(ndar_df) // 10) == 0:
            logger.info(f"Processing {idx} / {len(ndar_df)}")

        skip_subject = False
        subject_json = next(filter(lambda x: subject_id in str(x), subject_jsons))

        if subject_json is None:
            # print(f"Skipping {subject_id} because subject_json is None")
            skipped_subjects.append(
                {"subject_id": subject_id, "reason": "Cannot find subject_json"}
            )
            skip_subject = True
            continue

        # tracker checks
        tracker_row = qc_tracker_df[qc_tracker_df["subject"] == subject_id]
        if tracker_row.empty:
            skipped_subjects.append(
                {"subject_id": subject_id, "reason": "tracker_row empty"}
            )
            skip_subject = True
            # print(f"Skipping {subject_id} because tracker_row is empty")
            continue
        # inclusionexclusion_criteria_review_screening check
        inclusionexclusion_criteria_review_screening = tracker_row[
            "inclusionexclusion_criteria_review_screening"
        ].values[0]

        if not pd.isna(inclusionexclusion_criteria_review_screening):
            skipped_subjects.append(
                {
                    "subject_id": subject_id,
                    "reason": "inclusionexclusion_criteria_review_screening is"
                    f"{inclusionexclusion_criteria_review_screening}",
                }
            )
            skip_subject = True
            # print(f"Skipping {subject_id} because inclusionexclusion_criteria_review_screening"
            # f"is {inclusionexclusion_criteria_review_screening}")
            continue

        # psychs_p1p8_screening check
        psychs_p1p8_screening = tracker_row["psychs_p1p8_screening"].values[0]

        if not pd.isna(psychs_p1p8_screening):
            skipped_subjects.append(
                {
                    "subject_id": subject_id,
                    "reason": f"psychs_p1p8_screening is {psychs_p1p8_screening}",
                }
            )
            skip_subject = True
            # print(f"Skipping {subject_id} because psychs_p1p8_screening is"
            # f"{psychs_p1p8_screening}")
            continue

        # psychs_p9ac32_screening check
        psychs_p9ac32_screening = tracker_row["psychs_p9ac32_screening"].values[0]

        if not pd.isna(psychs_p9ac32_screening):
            skipped_subjects.append(
                {
                    "subject_id": subject_id,
                    "reason": f"psychs_p9ac32_screening is {psychs_p9ac32_screening}",
                }
            )
            skip_subject = True
            # print(f"Skipping {subject_id} because psychs_p9ac32_screening is "
            # f"{psychs_p9ac32_screening}")
            continue

        # subject_is_included
        chrcrit_included = get_variable_value(
            json_file=subject_json,
            redcap_event_name="screening",
            redcap_variable_name="chrcrit_included",
        )
        subject_is_included = chrcrit_included == "1"

        if not subject_is_included:
            skipped_subjects.append(
                {
                    "subject_id": subject_id,
                    "reason": f"chrcrit_included is {chrcrit_included}",
                }
            )
            skip_subject = True
            # print(f"Skipping {subject_id} because subject_is_included is False")
            continue

        if not skip_subject:
            selected_subjects.append(subject_id)
            new_ndar_df = pd.concat(
                [new_ndar_df, pd.DataFrame([row])], ignore_index=True
            )

    logger.info("Done filtering subjects")
    return selected_subjects, skipped_subjects, new_ndar_df


def print_summary(
    selected_subjects: List[str], skipped_subjects: List[Dict[str, Any]]
) -> None:
    """
    Prints a summary of the selected and skipped subjects

    Args:
        selected_subjects (List[str]): List of selected subjects
        skipped_subjects (List[Dict[str, Any]]): List of skipped subjects
    """

    logger.info("Summary:")
    logger.info(f"Selected {len(selected_subjects)} subjects")
    logger.info(f"Skipped {len(skipped_subjects)} subjects")

    summary_dict: Dict[str, int] = {}

    for skipped_data in skipped_subjects:
        reason = skipped_data["reason"]

        if reason not in summary_dict:
            summary_dict[reason] = 0

        summary_dict[reason] += 1

    # sort by count
    summary_dict = dict(
        sorted(summary_dict.items(), key=lambda item: item[1], reverse=True)
    )

    logger.info("Skipped reasons:")
    for reason, count in summary_dict.items():
        logger.info(f"{reason}: {count}")

    logger.info("Done printing summary")


if __name__ == "__main__":
    logger.info("Filtering ndar_subject01 based on selection criteria...")
    selected_subjects, skipped_subjects, new_ndar_df = select_subjects()

    logger.info(f"Selected {len(selected_subjects)} subjects")
    logger.info(f"Skipped {len(skipped_subjects)} subjects")

    new_ndar_csv_path = Path(DEST_CSV_PATH)
    new_ndar_df.to_csv(new_ndar_csv_path, index=False)
    logger.info(f"Saved new ndar_subject01 to {new_ndar_csv_path}")
    fix_ndar_csv(new_ndar_csv_path)

    print_summary(selected_subjects, skipped_subjects)

    logger.info("Done")
