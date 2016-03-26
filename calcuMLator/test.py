#!/bin/env python
'''
CalcuMLator testing file

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

FOLDER = os.path.dirname(__file__)+'/estimators/'
ADD_ESTIMATOR_PATH = FOLDER + 'add_estimator.pkl'
MUL_ESTIMATOR_PATH = FOLDER + 'mul_estimator.pkl'
# SUB_ESTIMATOR_PATH = FOLDER + 'sub_estimator.pkl'
# DIV_ESTIMATOR_PATH = FOLDER + 'div_estimator.pkl'


clf_add = joblib.load(ADD_ESTIMATOR_PATH)
clf_mul = joblib.load(MUL_ESTIMATOR_PATH)
# clf_sub = joblib.load(SUB_ESTIMATOR_PATH)
# clf_div = joblib.load(DIV_ESTIMATOR_PATH)

y_pred_add = clf_add.predict(data.X_test)
y_pred_mul = clf_mul.predict(data.X_test)
# y_pred_sub = clf_sub.predict(data.X_test)
# y_pred_div = clf_div.predict(data.X_test)

print(metrics.r2_score(data.y_test_add, y_pred_add))
print(metrics.r2_score(data.y_test_mul, y_pred_mul))
# print(metrics.r2_score(data.y_test_sub, y_pred_sub))
# print(metrics.r2_score(data.y_test_div, y_pred_div))

for i, j in zip(data.y_test_mul, y_pred_mul):
    print(i, j)
