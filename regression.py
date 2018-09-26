import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from parsing import data

# Generate dummy data
import numpy as np
import pandas as pd

# i_train, i_test = train_test_split(full_frame, test_size=0.5)
# short_i_train = i_train[['EXT_SOURCE_3', 'EXT_SOURCE_2', 'DAYS_EMPLOYED', 'DAYS_BIRTH', 'REGION_RATING_CLIENT_W_CITY', 'REGION_RATING_CLIENT', 'DAYS_LAST_PHONE_CHANGE']]
# short_i_test = i_test[['EXT_SOURCE_3', 'EXT_SOURCE_2', 'DAYS_EMPLOYED', 'DAYS_BIRTH', 'REGION_RATING_CLIENT_W_CITY', 'REGION_RATING_CLIENT', 'DAYS_LAST_PHONE_CHANGE']]
# o_train = i_train[['TARGET']] 
# o_test = i_test[['TARGET']] 
# i_train = i_train.drop(['TARGET'], axis=1)
# i_test = i_test.drop(['TARGET'], axis=1)
# print('shape -> ',i_train.shape)

def train(v):
    train_in_col = []
    train_out_col = ""
    model = Sequential()
    if 'train' in v:
        dict = v.get('train')
        if ('data' in dict) == False:
            return 'train element should have data'
        df = data[dict.get('data')].copy()
        df = df.drop(dict.get('skip'), axis=1)
        if(('validate' in dict) == True and dict.get('validate') == True):
            df, df_test = train_test_split(df, test_size=0.2)
            o_test = df_test[dict.get('output')]
            df_test = df_test.drop(dict.get('output'), axis=1)
        
        o = df[dict.get('output')]
        df = df.drop(dict.get('output'), axis=1)
        
        train_in_col = df.columns.values
        train_out_col = dict.get('output')  
        print('Training columns -> ',train_in_col)
        print('Output column -> ', train_out_col)
        dim = df.shape[1]
        model.add(Dense(dim *2 -1, input_dim=dim, kernel_initializer=dict.get('initializer'), activation=dict.get('activation')))
        model.add(Dense(dim -1, kernel_initializer=dict.get('initializer'), activation=dict.get('activation')))
        model.add(Dense(1, kernel_initializer=dict.get('initializer')))
        # Compile model
        model.compile(loss=dict.get('loss'), optimizer=dict.get('optimizer'), metrics=dict.get('metrics'))
        model.summary()

        model.fit(df, o, epochs=dict.get('epochs'), batch_size=5)
        print('model is trained now.')
        if(('validate' in dict) == True and dict.get('validate') == True):
            loss, acc = model.evaluate(df_test, o_test, batch_size=5)
            print('model is validated with loss %f and accuracy %f' % (loss, acc))

    if 'predict' in v:
        dict = v.get('predict')
        if ('data' in dict) == False:
            return 'predict element should have data'
        df = data[dict.get('data')].copy()
        df = df[train_in_col]
        data[dict.get('data')][train_out_col] = model.predict(df)
