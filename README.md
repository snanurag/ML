# Delete Rows
```
delete-rows :
  - data : cold_start_test
    in-col : temperature
    condition : is_temp_na
  - data : submission
    in-col : temperature
    condition : is_temp_na
  - data : submission
    in-col : prediction_window
    condition : daily
  - data : submission
    in-col : prediction_window
    condition : weekly
```
# Regression - Keras
```
keras:
  train :
    data : cold_start_test
    skip : [series_id, timestamp]
    output : consumption
    activation : tanh
    model : sequential
    initializer : normal
    loss : mean_squared_error
    optimizer : sgd
    metrics : [accuracy]
    validate : false
  predict :
    data : submission
```

# LGBMClassifier
```
lightgbm :
  train :
    data : cold_start_test
    skip : [series_id, timestamp]
    output : consumption
    type : LGBMClassifier
    learning-rate : 0.05
    reg-alpha : 0.1
    reg-lambda : 0.1
    subsample : 0.8
    n-estimators : 1000
    random-state : 50
  predict :
    data : submission
```

# LGBMRegressor
```
lightgbm :
  train :
    data : cold_start_test
    skip : [series_id, timestamp]
    output : consumption
    type : LGBMRegressor
  predict :
    data : submission
```
# Regression - xgboost (pretrain and train)
```
xgboost :
  pre-train:
    data : cold_start_test_temp_na
    skip : [series_id]
    output : consumption
    type : regression
  train :
    data : cold_start_test
    skip : [series_id]
    output : consumption
    type : regression
  predict :
    data : submission
```

# fillna
```
fillna :
  - data : cold_start_test
    value : -1
```

# Delete row on condition
```
# Takes array as input and return True against the values to delete and False for not to delete 
delete-rows :
  - data : cold_start_test
    in-col : temperature
    condition : is_temp_na
  - data : submission
    in-col : prediction_window
    condition : daily
```

# Full Sample yaml

```
data :
  read :
    - cold_start_test
    - consumption_train
    - meta
    - submission_format

ohe :
  - data : meta
    skip : 
      - series_id

customize-cell :
  - data : meta
    func : ohe_true_false

customize-column-cell-1 :
  - data : cold_start_test
    func : get_day_from_timestamp
    input : timestamp
    output : day

merge:
  left : cold_start_test
  right : meta
  how : left
  on : series_id

<!-- Takes series as input -->
customize-row :
  - data : cold_start_test
    func : replace_day_with_off

delete-columns :
  - data : cold_start_test
    columns:
      - monday_is_day_off
      - tuesday_is_day_off
      - wednesday_is_day_off
      - thursday_is_day_off
      - friday_is_day_off
      - saturday_is_day_off
      - sunday_is_day_off

<!-- Takes array as input and return True against the values to delete and False for not to delete  -->
delete-rows :
  - data : cold_start_test
    input : temperature
    condition : is_temp_na

customize-column-cell-2 :
  - data : cold_start_test
    func : get_date_from_timestamp
    input : timestamp
    outfile : cold_start_test_daily

group-by :
  - data : cold_start_test
    group-on :
      - timestamp
    aggregation:
      - consumption : sum
      - temperature : mean

csv :
    data :
      - cold_start_test
      - meta
    outfile :
     - cold_start_test_daily

lightgbm :
  data :
    - application_train
    - application_test
  dfs : bureau

```
