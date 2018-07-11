import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

# Generate dummy data
import numpy as np
import pandas as pd

# i_train = pd.read_csv('/Users/anurag/Documents/workspace/kaggle/Home_Credit_Default_Risk/Data/application_train.csv', index_col=[0,1]).as_matrix() 
# o_train = pd.read_csv('/Users/anurag/Documents/workspace/kaggle/Home_Credit_Default_Risk/Data/application_train.csv', usecols=[1]).as_matrix()
# i_test =  pd.read_csv('/Users/anurag/Documents/workspace/kaggle/Home_Credit_Default_Risk/Data/application_test.csv', index_col=[0]).as_matrix() 
cat1 = pd.read_csv('/Users/anurag/Documents/workspace/kaggle/Home_Credit_Default_Risk/Data/test.csv', index_col=[0]).as_matrix()
df = pd.DataFrame(cat1)
print(df)
df1 = df.apply(lambda x: pd.factorize(x)[0])
print(df1)
# cat2 = df1
# print(cat2)
cat3 = pd.read_csv('/Users/anurag/Documents/workspace/kaggle/Home_Credit_Default_Risk/Data/test2.csv', index_col=[0]).as_matrix()
df2 = pd.DataFrame(cat3)
print(df2.apply(lambda x: pd.factorize(x)[0]))

# x_train = np.random.random((1000, 20))
# y_train = keras.utils.to_categorical(np.random.randint(10, size=(1000, 1)), num_classes=10)
# x_test = np.random.random((100, 20))
# y_test = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(1, activation='relu', input_dim=120))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu'))
# model.add(Dropout(0.5))
# model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='sparse_categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(i_train, o_train,
          epochs=20,
          batch_size=128)
# model.predict()
# score = model.evaluate(x_test, y_test, batch_size=128)