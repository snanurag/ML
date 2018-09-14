import pandas as pd
import numpy as np
from parsing import data
from custom import custom

def apply_del_row(row):
    if np.isnan(row['temperature']) == True:
        return True
    else:
        return False

def concat(v):
    for a in v.get('data').get('dataframes'):
        data[v.get('data').get('target')] = pd.concat([data[v.get('data').get('target')], data[a]], ignore_index=True)

def delete(value):
    for a in value:
        if 'data' in a:
            if 'columns' in a:
                for e in a.get('columns'):
                    data[a.get('data')] = data[a.get('data')].drop([e], axis=1)

def delete_row(val):
    for a in val:
        conditional_method = getattr(custom, a.get('condition'))
        data[a.get('data')] = data[a.get('data')][conditional_method(data[a.get('data')][a.get('in-col')]) == False]

def fillna(v):
    for a in v:
        data[a.get('data')] = data[a.get('data')].fillna(a.get('value'))

def merge(value):
    for v in value:
        data[v.get('left')] = pd.merge(data[v.get('left')], data[v.get('right')], how=v.get('how'), on=v.get('on'))

def ohe(arr):
    df = pd.DataFrame()
    for dict in arr:
        for l in dict.get('skip'):
            df[l] = data[dict.get('data')][l]
            data[dict.get('data')] = data[dict.get('data')].drop([l],axis=1)
        data[dict.get('data')] = pd.get_dummies(data[dict.get('data')])
        for l in dict.get('skip'):
            data[dict.get('data')][l] = df[l]
 
def transfer(value):
    dict = value.get('from')
    df_from = data[dict.get('data')][dict.get('key')]
    from_col = dict.get('col') 
    df_from[from_col] = data[dict.get('data')][from_col]
    from_key = dict.get('key')

    dict = value.get('to')
    to_key = dict.get('key')
    data[dict.get('data')] = pd.merge(data[dict.get('data')], df_from, how='left', left_on=to_key, right_on=from_key, suffixes=('','_from'))
    
    for index, row in data[dict.get('data')].iterrows():
        if np.isnan(row[from_col+'_from']) == False:
            data[dict.get('data')].loc[index, from_col] = row[from_col+'_from']
    data[dict.get('data')] = data[dict.get('data')].drop([from_col+'_from'], axis=1)