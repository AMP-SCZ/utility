import json
import os
import shutil
import sys
from pathlib import Path
test_dir = Path(__file__).parent
code_dir = test_dir.parent
sys.path.append(str(code_dir))
from util import days_from_today_to_str_date, str_date_minus_str_date, \
        check_file_delay
from datetime import datetime, timedelta


def test_one():
    print(code_dir)

def test_today_minus_dateofscan():
    today_full = datetime.today()
    today_date = datetime.today().strftime('%Y-%m-%d')

    date_of_scan = '2011-09-16'
    date_of_scan_date_fmt = datetime.strptime(date_of_scan, '%Y-%m-%d')

    time_delta = -(today_full - date_of_scan_date_fmt)
    diff_days = time_delta.days



def test_str_date_minus_str_date():
    assert str_date_minus_str_date('2022-01-01', '2022-01-02') == 1
    assert str_date_minus_str_date('2022-01-02', '2022-01-01') == -1


def test_days_from_today_to_str_date():
    new_date = (datetime.today() - timedelta(days=0)).strftime('%Y-%m-%d')
    diff_days = str_date_minus_str_date(datetime.today().strftime('%Y-%m-%d'),
                                        new_date)
    assert diff_days == 0

    new_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    diff_days = str_date_minus_str_date(datetime.today().strftime('%Y-%m-%d'),
                                        new_date)
    assert diff_days == -1

    new_date = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
    diff_days = str_date_minus_str_date(datetime.today().strftime('%Y-%m-%d'),
                                        new_date)
    assert diff_days == -2

    diff_days = days_from_today_to_str_date(new_date)
    assert diff_days == -2


def test_check_file_delay():
    file = 'missing'
    new_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    print(check_file_delay(file, new_date))

