import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer

# Generate dummy data
import numpy as np
import pandas as pd
import os

df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/Data/bureau.csv')
# TODO Find the correlation with CREDIT_ACTIVE and CREDIT_TYPE as well.
df = df.drop(['CREDIT_CURRENCY', 'CREDIT_TYPE'], axis=1)

# print(df.shape)
df.loc[df['SK_ID_CURR'] == 100002].to_csv('test.csv')
print(df.loc[df['SK_ID_CURR'] == 100002])

df = df.groupby(['SK_ID_CURR']).sum()
# print(df.shape)
# print(df.loc[[215354]])

