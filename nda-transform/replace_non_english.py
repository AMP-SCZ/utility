#!/usr/bin/env python
"""
Rewrite the file to use latin-1 encoding, if UnicodeEncodeError is raised.
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path


def main():
    """
    Checks if a file can be encoded using 'latin-1' encoding. If not, it will
    replace the file with a new file that uses 'latin-1' encoding.

    The original file will be renamed to '.<filename>'

    Usage:
        python encode_to_latin.py <filename>

    Example:
        python encode_to_latin.py some_file.txt
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filename", help="The file to convert")
    args = parser.parse_args()

    filename = Path(args.filename)

    if not filename.exists():
        print(f"File {filename} does not exist")
        sys.exit(1)

    replace_file: bool = False
    with tempfile.NamedTemporaryFile("w", encoding="latin-1") as temp_file:
        with open(filename, "r", encoding="utf-8") as source_file:
            for idx, line in enumerate(source_file):
                try:
                    temp_file.write(line)
                except UnicodeEncodeError as e:
                    replace_file = True
                    print(f"Error: {e}")
                    print(f"Line {idx}: {line}")
                    temp_file.write(
                        line.encode("latin-1", errors="replace").decode("latin-1")
                    )

        if replace_file:
            print(f"Renaming {filename} to '.{filename}'")
            filename.rename(f".{filename}")

            temp_file.flush()
            temp_path = Path(temp_file.name)

            print(f"Saving 'utf-8' -> 'latin-1' -> 'utf-8' encoded file to {filename}")
            with tempfile.NamedTemporaryFile("w", encoding="utf-8") as temp_file_utf8:
                with open(temp_path, "r", encoding="latin-1") as temp_file_latin1:
                    temp_file_utf8.write(temp_file_latin1.read())

                temp_file_utf8.flush()
                shutil.copy(temp_file_utf8.name, filename)

    print("Done")
    return


if __name__ == "__main__":
    main()
