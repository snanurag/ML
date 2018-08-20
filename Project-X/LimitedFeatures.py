import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer

# Generate dummy data
import numpy as np
import pandas as pd
import bureau

full_frame = pd.read_csv('D:/Workspace/ML/Project-X/Data/application_train.csv', index_col=[0],)

def fact(x): 
    if x.dtype == np.object: return pd.factorize(x)[0] 
    else: return x

full_frame = full_frame.apply(fact)

# TARGET has same % defaulters for -6000 and abnormal no(365243) # calculated separately.
full_frame['DAYS_EMPLOYED'].replace({365243: -6000}, inplace = True)

full_frame = full_frame.fillna(full_frame.mean())
bureau_frame = bureau.df('bureau')
bureau_frame.fillna(0)
print("full frame shape before ->", full_frame.shape)
print("burea frame shape before ->",bureau_frame.shape)
mrged_frame = pd.merge(full_frame, bureau_frame, how='left', on='SK_ID_CURR')
print("merged frame shape -> ", mrged_frame.shape)

# Find correlations with the target and sort
correlations = mrged_frame.corr()['TARGET'].sort_values()

# Display correlations

print('Most Positive Correlations:\n', correlations.tail(25))
print('\nMost Negative Correlations:\n', correlations.head(25))


# i_train, i_test = train_test_split(full_frame, test_size=0.5)
# short_i_train = i_train[['EXT_SOURCE_3', 'EXT_SOURCE_2', 'DAYS_EMPLOYED', 'DAYS_BIRTH', 'REGION_RATING_CLIENT_W_CITY', 'REGION_RATING_CLIENT', 'DAYS_LAST_PHONE_CHANGE']]
# short_i_test = i_test[['EXT_SOURCE_3', 'EXT_SOURCE_2', 'DAYS_EMPLOYED', 'DAYS_BIRTH', 'REGION_RATING_CLIENT_W_CITY', 'REGION_RATING_CLIENT', 'DAYS_LAST_PHONE_CHANGE']]
# o_train = i_train[['TARGET']] 
# o_test = i_test[['TARGET']] 
# i_train = i_train.drop(['TARGET'], axis=1)
# i_test = i_test.drop(['TARGET'], axis=1)
# print('shape -> ',i_train.shape)

# model = Sequential()
# model.add(Dense(13, input_dim=7, kernel_initializer='normal', activation='tanh'))
# model.add(Dense(6, kernel_initializer='normal', activation='tanh'))
# model.add(Dense(1, kernel_initializer='normal'))
# # Compile model
# model.compile(loss='mean_squared_error', optimizer='sgd', metrics=["accuracy"])

# model.summary()


# model.fit(short_i_train, o_train, epochs=20, batch_size=100)
# loss, acc = model.evaluate(short_i_test, o_test, batch_size=100)
# o = model.predict(short_i_test)

# print ("loss -> ",loss)
# print("acc -> ", acc)
# np.savetxt("limited_feature.csv",o, delimiter=",")
