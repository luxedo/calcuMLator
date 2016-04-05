#!/bin/env python
'''
CalcuMLator training file

Copyright (C) 2016 Luiz Eduardo Amaral <luizamaral306@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import numpy as np
from sklearn import svm, grid_search, metrics, linear_model
from sklearn.externals import joblib
import os.path
import json
import data

FOLDER = os.path.dirname(os.path.abspath(__file__))+'/estimators/'

LINEAR_ADD_ESTIMATOR_PATH = FOLDER + 'linear_add_estimator.pkl'
SVC_ADD_ESTIMATOR_PATH = FOLDER + 'SVC_add_estimator.pkl'
NN_ADD_ESTIMATOR_PATH = FOLDER + 'NN_add_estimator.pkl'

def train_linear():
    '''
    creates the estimator for SVC
    '''
    param_grid = {'C': [3**x for x in range(15, 18)], 'gamma': [3**-x for x in range(6, 12)], 'kernel': ['rbf']}
    clf_linear_add = linear_model.LinearRegression()
    clf_linear_add.fit(data.X_train, data.y_train_add)
    joblib.dump(clf_linear_add, LINEAR_ADD_ESTIMATOR_PATH)
    return metrics.r2_score(data.y_test_add, clf_linear_add.predict(data.X_test))

def train_SVC():
    '''
    creates the estimator for SVC
    '''
    param_grid = {'C': [3**x for x in range(15, 18)], 'gamma': [3**-x for x in range(6, 12)], 'kernel': ['rbf']}
    svr = svm.SVR()
    clf_add = grid_search.RandomizedSearchCV(svr, param_grid)
    clf_add.fit(data.X_train, data.y_train_add)
    joblib.dump(clf_add, SVC_ADD_ESTIMATOR_PATH)
    return metrics.r2_score(data.y_test_add, clf_add.predict(data.X_test))

def train_NN():
    '''
    creates the estimator for SVC
    '''
    param_grid = {'C': [3**x for x in range(15, 18)], 'gamma': [3**-x for x in range(6, 12)], 'kernel': ['rbf']}
    svr = svm.SVR()
    clf_add = grid_search.RandomizedSearchCV(svr, param_grid)
    clf_add.fit(data.X_train, data.y_train_add)
    joblib.dump(clf_add, NN_ADD_ESTIMATOR_PATH)
    return metrics.r2_score(data.y_test_add, clf_add.predict(data.X_test))

r2_linear = train_linear()
print('Linear trained! r2 score: '+str(r2_linear))
r2_svc = train_SVC()
print('SVC trained! r2 score: '+str(r2_svc))
r2_nn = train_NN()
print('NN trained! r2 score: '+str(r2_nn))
