import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split

# Generate dummy data
import numpy as np
import pandas as pd

i_train = pd.read_csv('D:/Workspace/ML/Project-X/Data/application_train.csv', index_col=[0,1])
o_train = pd.read_csv('D:/Workspace/ML/Project-X/Data/application_train.csv', usecols=[1])
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

model = Sequential()
model.add(Dense(80, input_dim=120))
model.add(Activation("sigmoid"))
model.add(Dense(40))
model.add(Activation("softmax"))
model.add(Dense(1))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.1, nesterov=True)
model.compile(loss='mean_squared_error',
              optimizer=sgd,
              metrics=['accuracy'])

model.summary()

model.fit(i_train, o_train, epochs=100, batch_size=1000)

# o_test = model.predict(i_test)
# # score = model.evaluate(X_test, y_test, batch_size=128)
# print(o_test)