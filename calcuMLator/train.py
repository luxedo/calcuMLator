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
from sklearn.gaussian_process import GaussianProcess
from sklearn.neural_network import BernoulliRBM
from sklearn.externals import joblib
import data

FOLDER = path.dirname(path.realpath(__file__))+'/'
ESTIMATOR_FOLDER = FOLDER+'estimators/'
ESTIMATOR_CONF = FOLDER+'estimator_conf.json'
with open(ESTIMATOR_CONF) as text:
    conf = json.loads(text.read())

# data sets size
TRAINING_SIZE = 22
TRAINING_STEP = 3
TEST_SIZE = 10**3
TEST_RANGE = 10**3

# create training set
training_set = data.create_full_set(TRAINING_STEP, TRAINING_SIZE)
X_train, y_train_add, y_train_sub, y_train_mul, y_train_div = training_set

# create test set
test_set = data.create_random_set(TEST_RANGE, TEST_SIZE)
X_test, y_test_add, y_test_sub, y_test_mul, y_test_div = test_set


def train_linear(X_train, y_train, X_test, y_test):
    '''
    Creates the linear regression estimator and returns it along with it's r2_score
    '''
    clf_linear = linear_model.LinearRegression()
    clf_linear.fit(X_train, y_train)
    r2_linear = (metrics.r2_score(y_test, clf_linear.predict(X_test)), metrics.r2_score(y_train, clf_linear.predict(X_train)))
    coef_linear = {'coef': clf_linear.coef_.tolist(), 'intercept': clf_linear.intercept_}
    return clf_linear, r2_linear, coef_linear

def train_ridge(X_train, y_train, X_test, y_test):
    '''
    Creates ridge regression estimator and returns it along with it's r2_score
    '''
    clf_ridge = linear_model.RidgeCV()
    clf_ridge.fit(X_train, y_train)
    r2_ridge = metrics.r2_score(y_test, clf_ridge.predict(X_test)), metrics.r2_score(y_train, clf_ridge.predict(X_train))
    coef_ridge = {'coef': clf_ridge.coef_.tolist(), 'intercept': clf_ridge.intercept_, 'aplpha': clf_ridge.alpha_}
    return clf_ridge, r2_ridge, coef_ridge

def train_SVR(X_train, y_train, X_test, y_test):
    '''
    Creates the rbf estimator for SVR and returns it along with it's r2_score
    '''
    # xtrain, ytrain = X_train[:200], y_train[:200]
    clf_SVR = svm.SVR(C= 3**10, epsilon= 3**-2, kernel='rbf')
    clf_SVR.fit(X_train, y_train)
    r2_SVR = metrics.r2_score(y_test, clf_SVR.predict(X_test)), metrics.r2_score(y_train, clf_SVR.predict(X_train))
    coef_SVR = {'support_vectors': len(clf_SVR.support_vectors_), 'intercept': clf_SVR.intercept_.tolist()}
    return clf_SVR, r2_SVR, coef_SVR

def train_bagging(X_train, y_train, X_test, y_test):
    '''
    Creates bagging regressor estimator and returns it along with it's r2_score
    '''
    clf_bagging = ensemble.BaggingRegressor()
    clf_bagging.fit(X_train, y_train)
    r2_bagging = metrics.r2_score(y_test, clf_bagging.predict(X_test)), metrics.r2_score(y_train, clf_bagging.predict(X_train))
    coef_bagging = {'estimators': len(clf_bagging.estimators_), 'estimators_features': len(clf_bagging.estimators_features_)}
    return clf_bagging, r2_bagging, coef_bagging

def train_gaussian(X_train, y_train, X_test, y_test):
    '''
    Creates bagging regressor estimator and returns it along with it's r2_score
    '''
    clf_gaussian = GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-0)
    clf_gaussian.fit(X_train[:500], y_train[:500])
    r2_gaussian = metrics.r2_score(y_test, clf_gaussian.predict(X_test)), metrics.r2_score(y_train, clf_gaussian.predict(X_train))
    coef_gaussian = {'theta': clf_gaussian.theta_.tolist()}
    return clf_gaussian, r2_gaussian, coef_gaussian

def train_MLP(X_train, y_train, X_test, y_test):
    '''
    Creates the MLP estimator and returns it along with it's r2_score
    '''

def train_all():
    '''
    Trains all the estimators
    '''
    report = OrderedDict()
    coef = OrderedDict()
    # conf['estimators'] = ['linear', 'ridge', 'gaussian', 'bagging', 'SVR']
    conf['estimators'] = []
    for estimator in conf['estimators']:
        report[estimator] = OrderedDict()
        coef[estimator] = OrderedDict()
        for operator in conf['types'].values():
            # arguments - inject your code here!
            args = (X_train, eval('y_train_'+operator), X_test, eval('y_test_'+operator))
            estimator_path = ESTIMATOR_FOLDER+operator+'_'+conf[estimator]

            # create estimator - two evals?? seriously??
            clf, r2, c= eval('train_'+estimator+'(*args)')
            print(estimator+' '+operator+' trained! r2 score (test, train): '+str(r2))

            # save estimator
            joblib.dump(clf, estimator_path)
            report[estimator][operator] = r2
            coef[estimator][operator] = c
    with open(FOLDER+conf['report'], 'w') as text:
        text.write(json.dumps(report, indent=2))
    with open(FOLDER+conf['coef'], 'w') as text:
        text.write(json.dumps(coef, indent=2))

if __name__ == '__main__':
    train_all()
