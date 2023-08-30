#!/usr/bin/env python

import sys
from glob import glob
from tqdm import tqdm

# Example Usage:
# python parse_redcap_error.py /path/to/redcap-import-<JOBID>-*.out
# ./parse_redcap_error.py /path/to/redcap-import-<JOBID>-*.out

def parse_file(file) -> tuple:
    """
    Parses a file and returns a tuple containing the file path and the number of HTTP 400 errors found in the file.
    Expects redcap-import-*-*.out files.

    Args:
        file (str): The path to the file to be parsed.

    Returns:
        tuple: A tuple containing the file path and the number of HTTP 400 errors found in the file.
    """
    try:
        with open(file) as f:
            content = f.read().split('\n')
            error_count = 0

        for idx, line in enumerate(content):
            if 'HTTP Status: 400' in line:
                error_count += 1

                print('')
                print('\033[91m','Parsing',file,'\033[0m')
                print(content[idx-1].strip())
                print(content[idx+1])
                print('')

    except Exception as e:
        print(f"Error parsing file {file}: {e}")
        error_count = -1

    return (file, error_count)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <path/and*pattern.*>')
        sys.exit(1)

    files=glob(sys.argv[1])

    results = list(tqdm(map(parse_file, files), total=len(files)))

    print('Parsed ' +  str(len(files)) + ' files matching ' + sys.argv[1])
    for file, error_count in results:
        if error_count > 0:
            print(f"{file}: {error_count} errors")
        
