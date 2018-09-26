import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split

# Generate dummy data
import numpy as np
import pandas as pd

i_train = pd.read_csv('D:/Workspace/ML/Project-X/Data/application_train.csv', index_col=[0])
i_test =  pd.read_csv('D:/Workspace/ML/Project-X/Data/application_test.csv', index_col=[0])

full_frame = pd.concat([i_train, i_test])
def fact(x): 
    if x.dtype == np.object: return pd.factorize(x)[0] 
    else: return x

full_frame = full_frame.apply(fact)
full_frame.fillna(0) #TODO Not a correct approach

# TARGET has same % defaulters for -6000 and abnormal no(365243) # calculated separately.
full_frame['DAYS_EMPLOYED'].replace({365243: -6000}, inplace = True)

tmp = np.split(full_frame,[307511]) 
i_train = tmp[0]
i_test = tmp[1]

short_i_train = i_train[['DAYS_EMPLOYED', 'DAYS_BIRTH']]
short_o_train =  i_train[['TARGET']]
short_i_test = i_train[['DAYS_EMPLOYED', 'DAYS_BIRTH']]


model = Sequential()
model.add(Dense(3, input_dim=2, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
# Compile model
model.compile(loss='mean_squared_error', optimizer='sgd', metrics=["accuracy"])

model.summary()

model.fit(short_i_train, short_o_train, epochs=20, batch_size=1000)
o_test = model.predict(short_i_test)
np.savetxt("keras.csv", o_test, delimiter=",")