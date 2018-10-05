import pandas as pd
import numpy as np
from parsing import data
import sys,os

sys.path.append(os.getcwd())

def apply_del_row(row):
    if np.isnan(row['temperature']) == True:
        return True
    else:
        return False

def concat(v):
    for a in v.get('data').get('dataframes'):
        data[v.get('data').get('target')] = pd.concat([data[v.get('data').get('target')], data[a]], ignore_index=True)
        print('Data %s is concated to data %s' % (a, v.get('data').get('target')))

def delete(value):
    for a in value:
        if 'data' in a:
            if 'columns' in a:
                for e in a.get('columns'):
                    data[a.get('data')] = data[a.get('data')].drop([e], axis=1)

def delete_row(val):
    for a in val:
        conditional_method = getattr(__import__('custom.custom', globals(), locals(), [a.get('condition')]), a.get('condition'))
        col_arr = data[a.get('data')][a.get('in-col')]
        np_a = np.ndarray(col_arr.size, dtype=bool)
        count =0
        for i in col_arr:
            np_a[count] = conditional_method(i)
            count +=1
        data[a.get('data')] = data[a.get('data')][np_a == False]
        print('Row with condition %s on column %s is deleted' %(a.get('condition'), a.get('in-col')))

def fillna(v):
    for a in v:
        data[a.get('data')] = data[a.get('data')].fillna(a.get('value'))

def fillna_by_mean(v):
    for a in v:
        if 'search-in' in a:
            df = data[a.get('search-in')]
            df_grouped = df.groupby(a.get('group-on'))
            df = data[a.get('data')]
            for i, row in df.iterrows():
                for c in a.get('target'):
                    if np.isnan(row[c]):
                        # TODO Fix this 0 index
                        key = row[a.get('group-on')[0]]
                        if key in df_grouped.groups:
                            df.set_value(i, c, df_grouped.get_group(key)[c].mean()) 
        else:    
            df = data[a.get('data')]
            df[a.get('target')] = df.groupby(a.get('group-on'))[a.get('target')].transform(lambda x: x.fillna(x.mean()))
            data[a.get('data')] = df
    
# TODO it is failing because index is not unique.
def fillna_by_search(v):
    for a in v:
        df = data[a.get('data')]
        for search_k in a.get('search-in'):
            tmp_df = data[search_k].copy()
            df.set_index(a.get('match'), inplace=True)
            tmp_df.set_index(a.get('match'), inplace=True)
            tmp_itr = tmp_df.iterrows()
            val = next(tmp_itr)
            for i, row in df.iterrows():
                if np.isnan(row[a.get('col')]):
                    while val != None and val[0] <= i:
                        if val[0] == i and np.isnan(val[1][a.get('col')]) == False:
                            df.loc[i][a.get('col')] = val[1][a.get('col')]
                            # row[a.get('col')] = val[1][a.get('col')]
                            # df[i] = row
                            print('row %s is replaced ' % row)
                            try:
                                val = next(tmp_itr)
                            except StopIteration:
                                val = None
                            break
                        else:
                            try:
                                val = next(tmp_itr)
                            except StopIteration:
                                val = None
            df = df.reset_index(level=a.get('match'))
        data[a.get('data')] = df


# def fillna_by_search2(v):
#     for a in v:
#         df = data[a.get('data')]
#         df.set_index(a.get('match'), inplace=True)
#         for search_k in a.get('search-in'):
#             tmp_df = data[search_k].copy()
#             tmp_df.set_index(a.get('match'), inplace=True)
#             for index, row in df.iterrows():
#                 if np.isnan(row[a.get('col')]):
#                     val = tmp_df.loc[row[a.get('match')]][a.get('col')].mean()
#                     row[a.get('col')] = val
#                     df[index] = row 
#         df.reset_index(level=a.get('match'))                   

def group_by(v):
    for a in v:
        df = data[a.get('data')]
        if 'aggregation' in a:
            data[a.get('data')] = df.groupby(a.get('group-on'), as_index=a.get('as-index')).agg(a.get('aggregation'))
        else:
            data[a.get('data')] = df.groupby(a.get('group-on'), as_index=a.get('as-index')).mean()
       
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