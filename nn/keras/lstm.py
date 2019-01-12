import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense
from parsing import data
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

# progress bar
from tqdm import tqdm

# TODO make it generic. Right now, it is Power Laws prob specific
def train(v):
    dict = v.get('train')
    num_neurons = len(dict.get('input'))
    batch_size = 1
    batch_input_shape = (batch_size,1,num_neurons)
    df_pred = pd.DataFrame()
    if ('load' in v) == False:
        model = Sequential()
        # add LSTM layer - stateful MUST be true here in 
        # order to learn the patterns within a series
        model.add(LSTM(units=num_neurons, 
                batch_input_shape=batch_input_shape, 
                stateful=True))
        # followed by a dense layer with a single output for regression
        model.add(Dense(1))

        # compile
        model.compile(loss='mean_absolute_error', optimizer='adam')
    else :
        model = load_model(v.get('load')+".h5")

    epoch = dict.get('epoch')

    for i in tqdm(range(epoch), total=epoch, 
              desc='Learning Consumption Trends - Epoch'):
    
        # reset the LSTM state for training on each series
        train_data = data[dict.get('data')]
        if 'predict' in dict:
            predict_data = data[dict.get('predict')]
        trainingGroups = train_data.groupby(dict.get('seq-on'))
        trainingGroupSize = trainingGroups.ngroups
        for ser_id, ser_data in tqdm(train_data.groupby(dict.get('seq-on')),
                                        total=trainingGroupSize, desc="Training Groups progress"):
            scaler = MinMaxScaler(feature_range=(-1, 1))
            y = scaler.fit_transform(ser_data[dict.get('output')].values.reshape(-1, 1))
            X = ser_data[dict.get('input')]
            
            X = X.values.reshape(X.shape[0], 1, X.shape[1])

            model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
            if ('predict' in dict) == True:
                pred_subset = predict_data[predict_data[dict.get('seq-on')]==ser_id]
                pred_subset = pred_subset.set_index('pred_id')
                pred_subset = pred_subset[dict.get('input')]
                for i, row in pred_subset.iterrows():
                    y = model.predict(np.array([[row.values]]), batch_size=1)[0][0]
                    df_pred.set_value(i, 'pred_id', i)
                    df_pred.set_value(i, dict.get('output'), scaler.inverse_transform(y)[0][0])
            model.reset_states()
    data['submission_hr_pred'] = df_pred       
    df_pred.to_csv('submission_hr_pred.csv')

    if ('save' in dict) == True:        
        model.save(dict.get('save')+'.h5')


