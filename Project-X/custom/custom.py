import datetime


def generate_data_on_timestamp(x):
    d =  datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").date()
    return d.weekday()
    # print("generate_data_on_timestamp")
    # return "generate_data_on_timestamp"

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