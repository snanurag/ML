import pandas as pd
from parsing import data

def ohe(arr):
    df = pd.DataFrame()
    for dict in arr:
        for l in dict.get('skip'):
            df[l] = data[dict.get('data')][l]
            data[dict.get('data')] = data[dict.get('data')].drop([l],axis=1)
        data[dict.get('data')] = pd.get_dummies(data[dict.get('data')])
        for l in dict.get('skip'):
            data[dict.get('data')][l] = df[l]
 
def merge(value):
    data[value.get('left')] = pd.merge(data[value.get('left')], data[value.get('right')], how=value.get('how'), on=value.get('on'))

def delete(value):
    for a in value:
        if 'data' in a:
            if 'columns' in a:
                for e in a.get('columns'):
                    data[a.get('data')] = data[a.get('data')].drop([e], axis=1) 
