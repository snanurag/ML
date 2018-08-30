import pandas as pd
import os

df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/Data/cold_start_test.csv')
print(len(df['series_id'].unique()))

df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/Data/submission_format.csv')
print(len(df['series_id'].unique()))

df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/Data/meta.csv')
print(len(df['series_id'].unique()))

df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/Data/consumption_train.csv')
print(len(df['series_id'].unique()))