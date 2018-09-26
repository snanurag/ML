import pandas as pd
import xgboost as xgb
from parsing import data
from sklearn.model_selection import ShuffleSplit
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split


def train(v):
    if 'pre-train' in v:
        dict = v.get('pre-train')
        pDf = data[dict.get('data')].copy()
        pDf = pDf.drop(dict.get('skip'), axis=1)
        
        pLabels = pDf[dict.get('output')]
        pDf = pDf.drop(dict.get('output'), axis=1)
        
        train_in_col = pDf.columns.values
        train_out_col = dict.get('output')
        print('train in col : '+train_in_col+' out col : '+train_out_col)
        xg_train_0 = xgb.DMatrix(pDf, label=pLabels)

    if 'train' in v:
        dict = v.get('train')
        df = data[dict.get('data')].copy()
        df = df.drop(dict.get('skip'), axis=1)
        
        labels = df[dict.get('output')]
        df = df.drop(dict.get('output'), axis=1)
        
        train_in_col = df.columns.values
        train_out_col = dict.get('output')
        print('train in col : '+train_in_col+' out col : '+train_out_col)
    
    train_in, valid_in, train_o, valid_o = train_test_split(df, labels, test_size=0.05, random_state=42)


    xg_train_1 = xgb.DMatrix(train_in, label=train_o)
    xg_valid = xgb.DMatrix(valid_in, label=valid_o)

    params = {'objective': 'reg:gamma', 'verbose': False}
    if 'pre-train' in v:
        model_0 = xgb.train(params, xg_train_0, 30)
        model_0.save_model('model_0.model')

        params.update({'process_type': 'update',
                      'updater'     : 'refresh',
                      'refresh_leaf': True})
        model_1 = xgb.train(params, xg_train_1, 30, xgb_model=model_0)
    else:
        model_1 = xgb.train(params, xg_train_1, 30)

    print('full train\t',mse(model_1.predict(xg_valid), valid_o)) # benchmark
