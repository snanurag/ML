import pandas as pd
from os import path
import warnings
warnings.filterwarnings('ignore')

data_path = path.dirname(path.abspath(__file__)) +'/Data/'
data = {}

def read(list):
    for l in list:
        data[l] = pd.read_csv(data_path + l+".csv")
    return data

def read_limited(list):
    for l in list:
        data[l] = pd.read_csv(data_path + l+".csv", nrows=10000)
    return data
