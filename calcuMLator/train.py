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
from sklearn import svm, grid_search, metrics
from sklearn.externals import joblib
import os.path
import json
import data

FOLDER = os.path.dirname(os.path.abspath(__file__))+'/estimators/'
ADD_ESTIMATOR_PATH = FOLDER + 'add_estimator.pkl'
MUL_ESTIMATOR_PATH = FOLDER + 'mul_estimator.pkl'
# SUB_ESTIMATOR_PATH = FOLDER + 'sub_estimator.pkl'
# DIV_ESTIMATOR_PATH = FOLDER + 'div_estimator.pkl'

param_grid = {'C': [3**x for x in range(15, 18)], 'gamma': [3**-x for x in range(6, 12)], 'kernel': ['rbf']}

svr = svm.SVR()

clf_add = grid_search.RandomizedSearchCV(svr, param_grid)
clf_add.fit(data.X_train, data.y_train_add)

clf_mul = grid_search.RandomizedSearchCV(svr, param_grid)
clf_mul.fit(data.X_train, data.y_train_mul)

# clf_sub = grid_search.RandomizedSearchCV(svr, param_grid)
# clf_sub.fit(data.X_train, data.y_train_sub)

# clf_div = grid_search.RandomizedSearchCV(svr, param_grid)
# clf_div.fit(data.X_train, data.y_train_div)

print(metrics.r2_score(data.y_test_add, clf_add.predict(data.X_test)))
print(metrics.r2_score(data.y_test_mul, clf_mul.predict(data.X_test)))
# print(metrics.r2_score(data.y_test_sub, clf_sub.predict(data.X_test)))
# print(metrics.r2_score(data.y_test_div, clf_div.predict(data.X_test)))

joblib.dump(clf_add, ADD_ESTIMATOR_PATH)
joblib.dump(clf_mul, MUL_ESTIMATOR_PATH)
# joblib.dump(clf_sub, SUB_ESTIMATOR_PATH)
# joblib.dump(clf_div, DIV_ESTIMATOR_PATH)
