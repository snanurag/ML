import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split

# Generate dummy data
import numpy as np
import pandas as pd

# i_train = pd.read_csv('/Users/anurag/Documents/workspace/ML/Project-X/Data/test.csv', index_col=[0,1], dtype={'NAME_CONTRACT_TYPE': "category", 'CODE_GENDER': "category", 
# 'FLAG_OWN_CAR': "category",	'FLAG_OWN_REALTY': "category",   'NAME_TYPE_SUITE': "category",	'NAME_INCOME_TYPE': "category",	'NAME_EDUCATION_TYPE': "category",
# 	'NAME_FAMILY_STATUS': "category",	'NAME_HOUSING_TYPE': "category",    'OCCUPATION_TYPE': "category",   'WEEKDAY_APPR_PROCESS_START': "category",
#   'ORGANIZATION_TYPE': "category",  'FONDKAPREMONT_MODE': "category",	'HOUSETYPE_MODE': "category",  'WALLSMATERIAL_MODE': "category",	'EMERGENCYSTATE_MODE': "category"})
# o_train = pd.read_csv('/Users/anurag/Documents/workspace/ML/Project-X/Data/test.csv', usecols=[1])

i_train = pd.read_csv('/Users/anurag/Documents/workspace/ML/Project-X/Data/application_train.csv', index_col=[0,1])
o_train = pd.read_csv('/Users/anurag/Documents/workspace/ML/Project-X/Data/application_train.csv', usecols=[1])
i_test =  pd.read_csv('/Users/anurag/Documents/workspace/ML/Project-X/Data/application_test.csv', index_col=[0])

full_frame = pd.concat([i_train, i_test])
def fact(x): 
    if x.dtype == np.object: return pd.factorize(x)[0] 
    else: return x

full_frame = full_frame.apply(fact)
full_frame.fillna(0) #TODO Not a correct approach
# TARGET has same % defaulters for -6000 and abnormal no(365243) # calculated separately.
full_frame['DAYS_EMPLOYED'].replace({365243: -6000}, inplace = True)
# X_train, X_test, y_train, y_test = train_test_split(i_train, o_train, test_size=0.2, random_state=7)
tmp = np.split(full_frame,[307511]) 
i_train = tmp[0]
i_test = tmp[1]
model = Sequential()
model.add(Dense(1, input_shape=(120,)))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.1, nesterov=True)
model.compile(loss='mean_squared_error',
              optimizer=sgd,
              metrics=['accuracy'])

# model.fit(X_train, y_train,
#           epochs=10,
#           batch_size=128)
model.fit(i_train, o_train, epochs=10, batch_size=128)

o_test = model.predict(i_test)
# score = model.evaluate(X_test, y_test, batch_size=128)
print(o_test)