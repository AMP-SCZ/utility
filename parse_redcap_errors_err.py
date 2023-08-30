#!/usr/bin/env python

import sys
import re
from glob import glob
from tqdm import tqdm

# Example Usage:
# python parse_redcap_errors_err.py /path/to/redcap-import-<JOBID>-*.err
# ./parse_redcap_errors_err.py /path/to/redcap-import-<JOBID>-*.err

def parse_file(file_path) -> tuple:
    """
    Parses a file for errors and returns the file path and the number of errors found.
    Expects redcap-import-*-*.err files.

    Args:
        file_path (str): The path to the file to parse.

    Returns:
        tuple: A tuple containing the file path and the number of errors found.
    """
    try:
        with open(file_path) as file:
            content = file.read().split('\n')
            error_count = 0

        idx = 0
        while idx < len(content):
            line = content[idx]
            # If the line contains 'Traceback (most recent call last):', then there was an error
            if 'Traceback (most recent call last):' in line:
                error_count += 1

                print('')
                print('\033[91m','Parsing',file,'\033[0m')
                # Print the line before the error
                print(content[idx-1])
                
                # Skip to the next line that contains a .csv file name
                while not re.match(r'.*\.csv.*', content[idx+1]):
                    print(content[idx+1])
                    idx += 1                

                # Print the line after the error, with a csv file name
                print(content[idx+1])
                print('')

            idx += 1

    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        error_count = -1

    return (file_path, error_count)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python {__file__} <path/and*pattern.*>')
        sys.exit(1)

    files = glob(sys.argv[1])
    results = [parse_file(file) for file in tqdm(files)]

    # Print a brief summary of the results

    print(f"\nParsed {len(files)} files matching {sys.argv[1]}")

    errors_found = False
    errors_files_count = 0
    errors_found_count = 0
    for file, file_error_count in results:
        if file_error_count > 0:
            errors_found = True
            errors_files_count += 1
            errors_found_count += file_error_count
            print(f"{file}: {file_error_count} errors")

    print('\n')
    if not errors_found:
        print('\033[92m' + 'No errors found!' + '\033[0m')
    else:
        print('\033[91m' + f'{errors_files_count} files with errors found!\n# of errors: {errors_found_count}' + '\033[0m')
