import pandas as pd
from os import path
import warnings
import os
import numpy as np
warnings.filterwarnings('ignore')

data_path = path.dirname(path.abspath(__file__)) +'/Data/'
data = {}

def read(list):
    for l in list:
        data[l] = pd.read_csv(data_path + l+".csv")
        data[l] = convert_types(data[l])
    return data

def read_limited(list):
    for l in list:
        data[l] = pd.read_csv(data_path + l+".csv", nrows=10000)
        data[l] = convert_types(data[l])
    return data

def to_csv(value):
    for k, v in value.items():
        if k == "data":
            for o in v:
                output = path.dirname(path.abspath(__file__)) +'/output/'
                if path.exists(output) is False:
                    os.makedirs(output)
                data[o].to_csv(output+k+"_"+o+".csv")
             
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