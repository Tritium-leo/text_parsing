import typing
from datetime import datetime

format_str = ['%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']


def str_to_datetime(date_str: str):
    date_obj = None
    for one in format_str:
        try:
            date_obj = datetime.strptime(date_str, one)
            break
        except:
            pass
    return date_obj
