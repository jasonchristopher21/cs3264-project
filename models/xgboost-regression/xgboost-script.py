import numpy as np
import pandas as pd
import random

from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score

X_train = pd.read_csv('../../cleaned-data/X_train.csv')
y_train = pd.read_csv('../../cleaned-data/y_train.csv')

X_test = pd.read_csv('../../cleaned-data/X_test.csv')
y_test = pd.read_csv('../../cleaned-data/y_test.csv')

# Combine X and y to make sure that the oversampling is done correctly
X_train = pd.concat([X_train, y_train], axis=1)
X_test = pd.concat([X_test, y_test], axis=1)

columns_to_drop = ['land_use_label', 'subzone', 'planning_area', 'region',
       'temp_2024_04_07_min', 'temp_2024_04_07_max',
       'temp_2024_04_07_median', 'temp_2024_04_08_min', 'temp_2024_04_08_max',
       'temp_2024_04_08_median', 'temp_2024_04_09_min', 'temp_2024_04_09_max',
       'temp_2024_04_09_median', 'temp_2024_04_10_min', 'temp_2024_04_10_max',
       'temp_2024_04_10_median']

X_train = X_train.drop(columns=columns_to_drop)
X_test = X_test.drop(columns=columns_to_drop)

# Remove rows where min_ndvi values is -
X_train = X_train[X_train['min_ndvi'] != '-']
X_test = X_test[X_test['min_ndvi'] != '-']

# Split X and y
y_train = X_train['avg_temp']
X_train = X_train.drop(columns=['avg_temp'])

y_test = X_test['avg_temp']
X_test = X_test.drop(columns=['avg_temp'])

def set_data_types(X_train):
    X_train['tree cover'] = X_train['tree cover'].astype('int')
    X_train['grassland'] = X_train['grassland'].astype('int')
    X_train['shrubland'] = X_train['shrubland'].astype('int')
    X_train['cropland'] = X_train['cropland'].astype('int')
    X_train['built-up'] = X_train['built-up'].astype('int')
    X_train['permanent water bodies'] = X_train['permanent water bodies'].astype('int')
    X_train['herbaceous wetland'] = X_train['herbaceous wetland'].astype('int')
    X_train['herbaceous wetland'] = X_train['herbaceous wetland'].astype('int')
    X_train['bare / sparse vegetation'] = X_train['bare / sparse vegetation'].astype('int')
    X_train['min_ndvi'] = X_train['min_ndvi'].astype('float')
    X_train['mean_ndvi'] = X_train['mean_ndvi'].astype('float')
    X_train['max_ndvi'] = X_train['max_ndvi'].astype('float')
    X_train.drop(['snow and ice', 'mangroves', 'moss and lichen'], axis=1, inplace=True)
    return X_train

X_train = set_data_types(X_train)
X_test = set_data_types(X_test)

regressor = XGBRegressor()
regressor.fit(X_train, y_train)

# Predict and evaluate RMSE and R2 on test set
y_pred = regressor.predict(X_test)

# Calculate the RMSE
rmse = np.sqrt(np.mean((y_test - y_pred)**2))
print(f"RMSE: {rmse}")

# Calculate the R2
r2 = r2_score(y_test, y_pred)
print(f"R2: {r2}")