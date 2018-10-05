from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import gc
import pandas as pd
import numpy as np
from util import filterOnCorrelationLimit
from sklearn.metrics import mean_squared_error as mse
from parsing import data
import xgboost as xgb

def train(v):
    train_in_col = []
    train_out_col = ""
    if 'train' in v:
        dict = v.get('train')
        if ('data' in dict) == False:
            return 'train element should have data'
        df = data[dict.get('data')].copy()
        df = df.drop(dict.get('skip'), axis=1)
        
        labels = df[dict.get('output')]
        df = df.drop(dict.get('output'), axis=1)
        
        train_in_col = df.columns.values
        train_out_col = dict.get('output')  

    # Empty array for test predictions
    if 'predict' in v:
        dict2 = v.get('predict')
        if ('data' in dict2) == False:
            return 'predict element should have data'
        test = data[dict2.get('data')][train_in_col]
        
    # Empty array for out of fold validation predictions
    out_of_fold = np.zeros(df.shape[0])
    
    # Lists for recording validation and training scores
    valid_scores = []
    train_scores = []
    
    # Iterate through each fold
    if dict.get('type') == 'LGBMClassifier':
        # Create the kfold object
        k_fold = KFold(n_splits = 5, shuffle = True, random_state = 50)
        out_pred = np.zeros(test.shape[0])
        
        for train_indices, valid_indices in k_fold.split(df):
            # Training data for the fold
            train_in, train_o = df[train_indices], labels[train_indices]
            # Validation data for the fold
            valid_in, valid_o = df[valid_indices], labels[valid_indices]
            
            # Create the model
            model = lgb.LGBMClassifier(n_estimators=dict.get('n-estimators'), objective = 'binary', 
                                    class_weight = 'balanced', learning_rate = dict.get('learning-rate'), 
                                    reg_alpha = dict.get('reg-alpha'), reg_lambda = dict.get('reg-lambda'), 
                                    subsample = dict.get('subsample'), n_jobs = -1, random_state = dict.get('random-state'))
            
            # Train the model
            model.fit(train_in, train_o, eval_metric = 'auc',
                    eval_set = [(valid_in, valid_o)],
                    early_stopping_rounds = 100, verbose = 200)
            
            # Record the best iteration
            best_iteration = model.best_iteration_
                    
            # Make predictions
            out_pred += model.predict_proba(test, num_iteration = best_iteration)[:, 1] / k_fold.n_splits
            
            # Record the out of fold predictions
            out_of_fold[valid_indices] = model.predict_proba(valid_in, num_iteration = best_iteration)[:, 1]
            
            # Record the best score
            valid_score = model.best_score_['valid']['auc']
            train_score = model.best_score_['train']['auc']
            
            valid_scores.append(valid_score)
            train_scores.append(train_score)
            
            # Clean up memory
            gc.enable()
            del model, train_in, valid_in
            gc.collect()
            
        # Overall validation score
        valid_auc = roc_auc_score(labels, out_of_fold)
        
        # Add the overall scores to the metrics
        valid_scores.append(valid_auc)
        train_scores.append(np.mean(train_scores))
        
        # Needed for creating dataframe of validation scores
        fold_names = list(range(5))
        fold_names.append('overall')
        
        # Dataframe of validation scores
        metrics = pd.DataFrame({'fold': fold_names,
                                'train': train_scores,
                                'valid': valid_scores}) 
        print(metrics)

    elif dict.get('type') == 'LGBMRegressor':
        params = {
            'task': 'train',
            'boosting_type': 'gbdt',
            'objective': 'regression',
            'metric': {'l2', 'auc'},
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': 0
        }

        train_in, valid_in, train_o, valid_o = train_test_split(df, labels, test_size=0.2, random_state=42)
            
        lgb_train = lgb.Dataset(train_in, train_o)
        lgb_eval = lgb.Dataset(valid_in, valid_o, reference=lgb_train)
        model = lgb.train(params, lgb_train, num_boost_round=20,
            valid_sets=lgb_eval)
    
        print('full train\t',mse(model.predict(valid_in, num_iteration=model.best_iteration), valid_o)) # benchmark

        data[dict2.get('data')][train_out_col] = model.predict(test, num_iteration=model.best_iteration)

        print ('Lightgbm regression is done for %s \n' % dict.get('data'))