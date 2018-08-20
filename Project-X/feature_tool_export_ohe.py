# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
import os

# featuretools for automated feature engineering
import featuretools as ft

# matplotlit and seaborn for visualizations
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 22


# Suppress warnings from pandas
import warnings
warnings.filterwarnings('ignore')

from os import listdir
from os.path import isfile, join


def read_files(f):
    df = pd.read_csv(f)
    return df

mypath = os.path.dirname(os.path.abspath(__file__)) +'/Data/'
files = listdir(mypath)
data = {}

for file in files:
    # if file.lower().endswith('.csv'):
    if file.lower().endswith('bureau.csv') or file.lower().endswith('application_train.csv') or file.lower().endswith('application_test.csv') or file.lower().endswith('bureau_balance.csv'):
        data[file[:-4]] = read_files(mypath + file)

data['bureau'] = pd.get_dummies(data['bureau'])
data['bureau_balance'] = pd.get_dummies(data['bureau_balance'])

es = ft.EntitySet(id = 'clients_train')
es = es.entity_from_dataframe(entity_id = 'application_train', dataframe = data['application_train'], index = 'SK_ID_CURR')
es = es.entity_from_dataframe(entity_id = 'bureau', dataframe = data['bureau'], index = 'SK_ID_BUREAU')
es = es.entity_from_dataframe(entity_id = 'bureau_balance', dataframe = data['bureau_balance'], make_index = True, index = 'bureaubalance_index')

es = es.add_relationships([ft.Relationship(es['application_train']['SK_ID_CURR'], es['bureau']['SK_ID_CURR']), 
                            ft.Relationship(es['bureau']['SK_ID_BUREAU'], es['bureau_balance']['SK_ID_BUREAU'])])

feature_matrix, feature_names = ft.dfs(entityset = es, target_entity = 'application_train',
                       agg_primitives=['max', 'sum', 'min', 'mean'], max_depth = 1, features_only=False, verbose=True, chunk_size = len(data['application_train']))
print(feature_names)
feature_matrix.to_csv("feature_matrix_app_b_bb_ohe_train.csv")


es = ft.EntitySet(id = 'clients_test')
es = es.entity_from_dataframe(entity_id = 'application_test', dataframe = data['application_test'], index = 'SK_ID_CURR')
es = es.entity_from_dataframe(entity_id = 'bureau', dataframe = data['bureau'], index = 'SK_ID_BUREAU')
es = es.entity_from_dataframe(entity_id = 'bureau_balance', dataframe = data['bureau_balance'], make_index = True, index = 'bureaubalance_index')

es = es.add_relationships([ft.Relationship(es['application_test']['SK_ID_CURR'], es['bureau']['SK_ID_CURR']),
                          ft.Relationship(es['bureau']['SK_ID_BUREAU'], es['bureau_balance']['SK_ID_BUREAU'])])

feature_matrix, feature_names = ft.dfs(entityset = es, target_entity = 'application_test',
                       agg_primitives=['max', 'sum', 'min', 'mean'], max_depth = 1, features_only=False, verbose=True,  chunk_size = len(data['application_test']))
print(feature_names)
feature_matrix.to_csv("feature_matrix_aap_b_bb_ohe_test.csv")

print('==> %d Total Features' % len(feature_names))
print('==> Features -> ', feature_names)

# feature_matrix = feature_matrix.head(1000)
# print('==> feature_matrix shape ', feature_matrix.shape())