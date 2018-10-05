import pandas as pd
from os import path
from os import listdir
import warnings
import os
import numpy as np
warnings.filterwarnings('ignore')

data_path = os.getcwd() +'/Data/'
cache_path = os.getcwd() +'/.cache/'
data = {}
out_data = {}

def read(list):
    for l in list:
        if isinstance(l, dict) == True:
            for k, _ in l.items():
                data[k] = pd.read_csv(data_path + k+".csv", index_col=l.get('skip')) 
                data[k] = convert_types(data[k])
                break
        elif isinstance(l, str) == True:
            data[l] = pd.read_csv(data_path + l+".csv")
            data[l] = convert_types(data[l])
    print('Read all data.')
    return data

def read_limited(list):
    for l in list:
        if isinstance(l, dict) == True:
            for k, _ in l.items():
                data[k] = pd.read_csv(data_path + k+".csv", index_col=l.get('skip'), nrows=10000) 
                data[k] = convert_types(data[k])
                break
        elif isinstance(l, str) == True:
            data[l] = pd.read_csv(data_path + l+".csv", nrows=10000)
            data[l] = convert_types(data[l])
    return data

def read_from_cache():
    files = listdir(cache_path)
    for k in files:
        data[k] = pd.read_csv(cache_path + k)
    print('Read from cache.')

def cache_data():
    if path.exists(cache_path) is False:
        os.makedirs(cache_path)
    for k in data:
        data[k].to_csv(cache_path+k, index=False)
    print('cache is generated.')

def delete_df(v):
    for x in v.get('data'):
        del data[x]

def to_csv(dict):
    output = os.getcwd() +'/output/'
    if path.exists(output) is False:
        os.makedirs(output)
    v = dict.get('data')
    ind = dict.get('index')
    for o in v:
        data[o].to_csv(output+o+".csv", index=ind)
        print("csv is generated for %s" % o)

def copy(val):
    for v in val:
        data[v.get('to')] = data[v.get('from')].copy()

            
def convert_types(df):
    """Convert pandas data types for memory reduction."""

    # Iterate through each column
    for c in df:

        # Booleans mapped to integers
        if set(df[c].unique()) == {0, 1}:
            df[c] = df[c].astype(bool)

        # Float64 to float32
        elif df[c].dtype == float:
            df[c] = df[c].astype(np.float32)

        # Int64 to int32
        elif df[c].dtype == int:
            df[c] = df[c].astype(np.int32)
        
        # # Convert objects to category
        # elif (df[c].dtype == 'object') and (df[c].nunique() < df.shape[0]):
        #     df[c] = df[c].astype('category')
    return df