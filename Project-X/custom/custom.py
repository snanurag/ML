import datetime
import numpy as np
import pandas as pd

def get_day_from_timestamp(x):
    return pd.to_datetime(x, format="%Y-%m-%d %H:%M:%S").dayofweek

def get_week_from_timestamp(x):
    return pd.to_datetime(x, format="%Y-%m-%d %H:%M:%S").week

def get_date_from_timestamp(x):
    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").date()

def ohe_true_false(x):
    if type(x) == bool:
        return int(x == True)
    else:
        return x

def replace_day_with_off(row):
    if row['day'] == 0 and row['monday_is_day_off'] == 0:
        row['day'] = 1
    elif row['day'] == 1 and row['tuesday_is_day_off'] == 0:
        row['day'] = 1
    elif row['day'] == 2 and row['wednesday_is_day_off'] == 0:
        row['day'] = 1
    elif row['day'] == 3 and row['thursday_is_day_off'] == 0:
        row['day'] = 1
    elif row['day'] == 4 and row['friday_is_day_off'] == 0:
        row['day'] = 1
    elif row['day'] == 5 and row['saturday_is_day_off'] == 0:
        row['day'] = 1
    elif row['day'] == 6 and row['sunday_is_day_off'] == 0:
        row['day'] = 1
    else:
        row['day'] = 0
    return row

# Takes array as input
def is_temp_na(x):   
    return np.isnan(x)

def daily(x):
    return x == 'daily'

def weekly(x):
    return x == 'weekly'
