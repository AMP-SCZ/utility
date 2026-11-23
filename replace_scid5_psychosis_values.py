#!/usr/bin/env python

import sys
import pandas as pd

if len(sys.argv)==1 or sys.argv[1] in ['-h','--help']:
    print("""This script removes incompatible date and number values from RPMS scid5_psychosis_mood_substance_abuse form.
Usage:
__file__ AB12345_scid5_psychosis_mood_substance_abuse.csv
""")
    exit(0)

df= pd.read_csv(sys.argv[1])


