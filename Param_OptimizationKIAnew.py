#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:59:25 2020

@author: vijay
"""

# Importing the libraries
import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV

response_data2 = pd.read_csv('Huh7_WT_Fzd2.csv')
drug_list2 = response_data2.iloc[:, 0].values
alldrugs2 = pd.read_csv('kir_allDrugs_namesDoses.csv', encoding='latin1')

alldrugs2 = alldrugs2.set_index('compound')
dataset2 = alldrugs2.loc[drug_list2]
response2 = response_data2['Huh7 WT'].values
dataset2["response"] = response2

# Importing the dataset
X2 = dataset2.iloc[:, 0:298].values
y2 = dataset2.iloc[:, 298].values


def build_classifier(optimizer, init, activation, hl):
    classifier = Sequential()
    classifier.add(Dense(units = hl, kernel_initializer = init, activation = activation, input_dim = 298))
    classifier.add(Dense(units = hl, kernel_initializer = init, activation = activation))
    classifier.add(Dense(units = 1, kernel_initializer = init))
    classifier.compile(loss = 'mean_squared_error', optimizer= optimizer, metrics=[ 'mse'])
    return classifier
model = KerasRegressor(build_fn=build_classifier)
param_grid = {'batch_size': [2], 
              'init': ['uniform', 'TruncatedNormal', 'normal', 'lecun_uniform', 'glorot_normal', 'he_normal', 'glorot_uniform', 'VarianceScaling', 'orthogonal', 'he_uniform'],
              'epochs': [120], 
              'activation': ['relu', 'elu', 'selu'], 
              'optimizer': ['rmsprop','adagrad', 'adamax', 'adadelta', 'adam', 'nadam'], 
              'hl': [100]}
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs= 24, cv=44)
grid_result = grid.fit(X2, y2)

print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']

print(means)
    
best_parameters = grid_result.best_params_
best_accuracy = grid_result.best_score_

for k, v in best_parameters.items():
    print(k, v)
