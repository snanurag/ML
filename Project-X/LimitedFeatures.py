import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split

# Generate dummy data
import numpy as np
import pandas as pd

full_frame = pd.read_csv('D:/Workspace/ML/Project-X/Data/application_train.csv', index_col=[0],)

def fact(x): 
    if x.dtype == np.object: return pd.factorize(x)[0] 
    else: return x

full_frame = full_frame.apply(fact)
full_frame = full_frame.fillna(0) #TODO Not a correct approach

# TARGET has same % defaulters for -6000 and abnormal no(365243) # calculated separately.
full_frame['DAYS_EMPLOYED'].replace({365243: -6000}, inplace = True)

# full_frame = np.square(full_frame)
# full_frame.loc[:,'EXT_SOURCE_3'] *= 100

# Find correlations with the target and sort
correlations = full_frame.corr()['TARGET'].sort_values()

# Display correlations
print('Most Positive Correlations:\n', correlations.tail(25))
print('\nMost Negative Correlations:\n', correlations.head(25))


i_train, i_test = train_test_split(full_frame, test_size=0.5)
short_i_train = i_train[['EXT_SOURCE_3', 'EXT_SOURCE_2', 'DAYS_EMPLOYED', 'DAYS_BIRTH']]
short_i_test = i_test[['EXT_SOURCE_3', 'EXT_SOURCE_2', 'DAYS_EMPLOYED', 'DAYS_BIRTH']]
o_train = i_train[['TARGET']] 
o_test = i_test[['TARGET']] 
i_train = i_train.drop(['TARGET'], axis=1)
i_test = i_test.drop(['TARGET'], axis=1)
print('shape -> ',i_train.shape)

model = Sequential()
model.add(Dense(120, input_dim=120, kernel_initializer='normal', activation='tanh'))
model.add(Dense(60, kernel_initializer='normal', activation='tanh'))
model.add(Dense(1, kernel_initializer='normal'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='sgd', metrics=["accuracy"])

model.summary()


model.fit(i_train, o_train, epochs=50, batch_size=100)
loss, acc = model.evaluate(i_test, o_test, batch_size=100)
print ("loss -> ",loss)
print("acc -> ", acc)
o = model.predict(i_test)
np.savetxt("limited_feature.csv",o, delimiter=",")
