from datetime import datetime
from pathlib import Path
import pandas as pd
import json


def get_consent(arg):
    
    if isinstance(arg,pd.DataFrame):
        df=arg
    else:
        df=pd.read_csv(arg, dtype=str)
    # df can contain Young Patient's and/or Guardian's rows
    
    # sort in ascending order
    df_sorted= df.sort_values('interview_date',
        key=lambda dates: [datetime.strptime(x,'%m/%d/%Y') for x in dates])
    
    chr_hc= df_sorted.iloc[-1]['group']

    return df_sorted, chr_hc


def str_date_minus_str_date(date_str1: str, date_str2: str) -> int:
    '''Get time delta between dates in string:  (date_str2 - date_str1)'''
    date1 = datetime.strptime(date_str1, '%Y-%m-%d')
    date2 = datetime.strptime(date_str2, '%Y-%m-%d')

    time_delta = (date2 - date1)
    diff_days = time_delta.days+1

    return diff_days


