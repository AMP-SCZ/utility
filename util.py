from datetime import datetime


def str_date_minus_str_date(date_str1: str, date_str2: str) -> int:
    '''Get time delta between dates in string:  -(date_str1 - date_str2)'''
    date1 = datetime.strptime(date_str1, '%Y-%m-%d')
    date2 = datetime.strptime(date_str2, '%Y-%m-%d')

    time_delta = -(date1 - date2)
    diff_days = time_delta.days

    return diff_days


def days_from_today_to_str_date(date_str: str) -> int:
    '''Get time delta from today to a date in string format'''
    diff_days = str_date_minus_str_date(datetime.today().strftime('%Y-%m-%d'),
                                        date_str)
    return diff_days


