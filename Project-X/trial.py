import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split

# Generate dummy data
import numpy as np
import pandas as pd


i_train = pd.read_csv('/Users/anurag/Documents/workspace/ML/Project-X/Data/application_train.csv')

anom_1 = i_train[i_train['DAYS_EMPLOYED'] < -8000]
print('The non-anomalies default on %0.2f%% of loans' % (100 * anom_1['TARGET'].mean()))

anom_2 = i_train[i_train['DAYS_EMPLOYED'] < -4000]
anom_2 = pd.concat([anom_1, anom_2]).drop_duplicates(keep=False)
print('The non-anomalies default on %0.2f%% of loans' % (100 * anom_2['TARGET'].mean()))

anom = i_train[i_train['DAYS_EMPLOYED'] == 365243]
non_anom = i_train[i_train['DAYS_EMPLOYED'] != 365243]
print('The non-anomalies default on %0.2f%% of loans' % (100 * non_anom['TARGET'].mean()))
print('The anomalies default on %0.2f%% of loans' % (100 * anom['TARGET'].mean()))