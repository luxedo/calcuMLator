#!/bin/env python2
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
from os import path, remove, listdir
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import TheilSenRegressor
from sklearn.linear_model import PassiveAggressiveRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.cross_decomposition import PLSRegression
from sklearn.neural_network import MLPRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import r2_score
from sklearn.externals import joblib
import data

VERSION = 'v2.0'
FOLDER = path.dirname(path.realpath(__file__))+'/'
ESTIMATOR_FOLDER = FOLDER+'estimators/'
ESTIMATOR_CONF = FOLDER+'estimator_conf.json'
with open(ESTIMATOR_CONF) as text:
    conf = json.loads(text.read())

# data sets size
TRAINING_SIZE = 10**3
TRAINING_RANGE = 10**3
TEST_SIZE = 10**3
TEST_RANGE = 10**3

# create training set
training_set = data.create_random_set(TRAINING_RANGE, TRAINING_SIZE)
X_train, y_train_add, y_train_sub, y_train_mul, y_train_div = training_set

# create test set
test_set = data.create_random_set(TEST_RANGE, TEST_SIZE)
X_test, y_test_add, y_test_sub, y_test_mul, y_test_div = test_set

# training configurations: linear
knnr_args = {'training_function': KNeighborsRegressor,
             'return_coefficients': {},
             'training_arguments': None}
linear_args = {'training_function': LinearRegression,
               'return_coefficients': {'coef': 'coef_',
                                       'intercept': 'intercept_'},
               'training_arguments': None}
ridge_args = {'training_function': RidgeCV,
              'return_coefficients': {'coef': 'coef_',
                                      'intercept': 'intercept_',
                                      'aplpha': 'alpha_'},
              'training_arguments': None}
lasso_args = {'training_function': LassoCV,
              'return_coefficients': {'coef': 'coef_',
                                      'intercept': 'intercept_',
                                      'aplpha': 'alpha_'},
              'training_arguments': None}
elastic_args = {'training_function': ElasticNetCV,
                'return_coefficients': {'coef': 'coef_',
                                        'alpha': 'alpha_',
                                        'l1_ratio': 'l1_ratio_',
                                        'intercept': 'intercept_'},
                'training_arguments': None}
bayesian_args = {'training_function': BayesianRidge,
                 'return_coefficients': {'coef': 'coef_',
                                         'alpha': 'alpha_',
                                         'lambda': 'lambda_',
                                         'intercept': 'intercept_'},
                 'training_arguments': None}
theil_args = {'training_function': TheilSenRegressor,
              'return_coefficients': {'coef': 'coef_',
                                      'breakdown': 'breakdown_',
                                      'n_subpopulation': 'n_subpopulation_',
                                      'intercept': 'intercept_'},
              'training_arguments': None}
PAR_args = {'training_function': PassiveAggressiveRegressor,
            'return_coefficients': {'coef': 'coef_',
                                    'intercept': 'intercept_'},
            'training_arguments': {'C': 10}}
SVR_args = {'training_function': SVR,
            'return_coefficients': {'support_vectors':
                                    'support_vectors_',
                                    'intercept': 'intercept_'},
            'training_arguments': {'C': 3**6, 'epsilon': 3**-3,
                                   'kernel': 'rbf', 'gamma': 3**-8}}
bagging_args = {'training_function': BaggingRegressor,
                'return_coefficients': {},
                'training_arguments': None}
gaussian_args = {'training_function': GaussianProcessRegressor,
                 'return_coefficients': {'alpha': 'alpha_'},
                 'training_arguments': {'kernel': RBF()}}
dtree_args = {'training_function': DecisionTreeRegressor,
              'return_coefficients': {'n_outputs': 'n_outputs_'},
              'training_arguments': None}
PLS_args = {'training_function': PLSRegression,
            'return_coefficients': {'coef': 'coef_'},
            'training_arguments': None}
MLP_args = {'training_function': MLPRegressor,
            'return_coefficients': {'coefs': 'coefs_[0]',
                                    'intercepts': 'intercepts_[0]',
                                    'n_layers': 'n_layers_'},
            'training_arguments': None}
k_ridge_args = {'training_function': KernelRidge,
                'return_coefficients': {'dual_coef': 'dual_coef_'},
                'training_arguments': {'kernel': 'poly'}}
forest_args = {'training_function': RandomForestRegressor,
               'return_coefficients': {},
               'training_arguments': None}

train_args = {'linear': linear_args, 'ridge': ridge_args, 'lasso': lasso_args,
              'elastic': elastic_args, 'bayesian': bayesian_args,
              'theil': theil_args, 'PAR': PAR_args, 'SVR': SVR_args,
              'bagging': bagging_args, 'gaussian': gaussian_args,
              'dtree': dtree_args, 'PLS': PLS_args, 'MLP': MLP_args,
              'knnr': knnr_args, 'k_ridge': k_ridge_args,
              'forest': forest_args}


def trainer(X_train, y_train, X_test, y_test, training_function,
            return_coefficients, training_arguments=None):
    '''
    Trains the estimators in the arguments
    '''
    if training_arguments:
        estimator = training_function(**training_arguments)
    else:
        estimator = training_function()
    estimator.fit(X_train, y_train)
    r2 = (round(r2_score(y_test, estimator.predict(X_test)), 5),
          round(r2_score(y_train, estimator.predict(X_train)), 5))
    coefficients = {}
    for key, value in return_coefficients.items():
        coefficients[key] = np.array(eval('estimator.'+value)).tolist()
    return estimator, r2, coefficients


def run_trainer(name, report, coef):
    # delete old files
    print 'Deleting files'
    for filename in listdir(ESTIMATOR_FOLDER):
        if name in filename:
            remove(ESTIMATOR_FOLDER+filename)
    print 'Training '+name
    report[name] = OrderedDict()
    coef[name] = OrderedDict()
    for operator in conf['types'].values():
        # arguments - inject your code here!
        data_args = (X_train, eval('y_train_'+operator),
                     X_test, eval('y_test_'+operator))
        name_path = ESTIMATOR_FOLDER+operator+'_'+conf[name]

        clf, r2, c = trainer(*data_args, **train_args[name])
        print(name+' '+operator+' trained! r2 score (test, train): ' +
              str(r2))
        # save estimator
        joblib.dump(clf, name_path)
        report[name][operator] = r2
        coef[name][operator] = c


def train_all():
    '''
    Trains all the estimators
    '''
    report = OrderedDict()
    coef = OrderedDict()
    # conf['estimators'] = ['k_ridge']
    for estimator_name in conf['estimators']:
        run_trainer(estimator_name, report, coef)

    with open(FOLDER+conf['report'], 'w') as text:
        text.write(json.dumps(report, indent=2))
    with open(FOLDER+conf['coef'], 'w') as text:
        text.write(json.dumps(coef, indent=2))

if __name__ == '__main__':
    train_all()
    # run_trainer('SVR', {}, {})
