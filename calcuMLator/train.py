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
import json
from collections import OrderedDict
from os import path
import numpy as np
from sklearn import svm, grid_search, metrics, linear_model, ensemble
from sklearn.externals import joblib
from data import *

FOLDER = path.dirname(path.realpath(__file__))+'/'
ESTIMATOR_FOLDER = FOLDER+'estimators/'
ESTIMATOR_CONF = FOLDER+'estimator_conf.json'
with open(ESTIMATOR_CONF) as text:
    conf = json.loads(text.read())


def train_linear(X_train, y_train, X_test, y_test):
    '''
    Creates the linear regression estimator and returns it along with it's r2_score
    '''
    clf_linear = linear_model.LinearRegression()
    clf_linear.fit(X_train, y_train)
    r2_linear = metrics.r2_score(y_test, clf_linear.predict(X_test))
    return clf_linear, r2_linear

def train_SVR(X_train, y_train, X_test, y_test):
    '''
    Creates the rbf estimator for SVR and returns it along with it's r2_score
    '''
    clf_SVR = svm.SVR()
    clf_SVR.fit(X_train, y_train)
    r2_SVR = metrics.r2_score(y_test, clf_SVR.predict(X_test))
    return clf_SVR, r2_SVR

def train_bagging(X_train, y_train, X_test, y_test):
    '''
    Creates ensemble regressor estimator and returns it along with it's r2_score
    '''
    clf_bagging = ensemble.BaggingRegressor()
    clf_bagging.fit(X_train, y_train)
    r2_bagging = metrics.r2_score(y_test, clf_bagging.predict(X_test))
    return clf_bagging, r2_bagging

def train_ridge(X_train, y_train, X_test, y_test):
    '''
    Creates ridge regression estimator and returns it along with it's r2_score
    '''
    clf_ridge = linear_model.RidgeCV()
    clf_ridge.fit(X_train, y_train)
    r2_ridge = metrics.r2_score(y_test, clf_ridge.predict(X_test))
    return clf_ridge, r2_ridge

def train_bayesian(X_train, y_train, X_test, y_test):
    '''
    Creates ridge regression estimator and returns it along with it's r2_score
    '''
    clf_bayesian = linear_model.BayesianRidge()
    clf_bayesian.fit(X_train, y_train)
    r2_bayesian = metrics.r2_score(y_test, clf_bayesian.predict(X_test))
    return clf_bayesian, r2_bayesian

def train_lars(X_train, y_train, X_test, y_test):
    '''
    Creates ridge regression estimator and returns it along with it's r2_score
    '''
    clf_lars = linear_model.LarsCV()
    clf_lars.fit(X_train, y_train)
    r2_lars = metrics.r2_score(y_test, clf_lars.predict(X_test))
    return clf_lars, r2_lars


def train_MLP(X_train, y_train, X_test, y_test):
    '''
    Creates the MPL estimator and returns it along with it's r2_score
    '''

def train_all():
    '''
    Trains all the estimators
    '''
    report = OrderedDict()
    for estimator in conf['estimators']:
        report[estimator] = OrderedDict()
        for operator in conf['types'].values():
            # arguments - inject your code here!
            args = (X_train, eval('y_train_'+operator), X_test, eval('y_test_'+operator))
            estimator_path = ESTIMATOR_FOLDER+operator+'_'+conf[estimator]

            # create estimator - two evals?? seriously??
            clf, r2 = eval('train_'+estimator+'(*args)')
            print(estimator+' '+operator+' trained! r2 score: '+str(r2))

            # save estimator
            joblib.dump(clf, estimator_path)
            report[estimator][operator] = r2
    with open(FOLDER+conf['report'], 'w') as text:
        text.write(json.dumps(report, indent=2))

if __name__ == '__main__':
    train_all()
