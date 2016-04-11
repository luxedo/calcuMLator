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
import argparse
import json
from os import path
from sklearn.externals import joblib

FOLDER = path.dirname(path.realpath(__file__))+'/'
ESTIMATOR_FOLDER = FOLDER+'estimators/'
ESTIMATOR_CONF = FOLDER+'estimator_conf.json'
with open(ESTIMATOR_CONF) as text:
    conf = json.loads(text.read())

def predict(number1, number2, operator, estimator):
    '''
    Predicts the value of the operation
    '''
    args = np.array([number1, number2]).reshape(1, -1)
    if estimator in conf['estimators'] and operator in conf['types']:
        estimator_path = ESTIMATOR_FOLDER+conf['types'][operator]+'_'+conf[estimator]
        clf = joblib.load(estimator_path)
        return clf.predict(args)[0]
    else:
        return 0

def main():
    parser = argparse.ArgumentParser(description='Calculates the operation using Machine Learning')
    parser.add_argument('number1', metavar='N1', help='a number for the calculation')
    parser.add_argument('operator', metavar='OP', help='The operator for the calculation (+, -, *, /)')
    parser.add_argument('number2', metavar='N2', help='a number for the calculation')
    parser.add_argument('estimator', metavar='E', help='The estimator for the calculation (linear, SVR)')
    args = parser.parse_args()

    try:
        number1 = float(args.number1)
        operator = args.operator
        number2 = float(args.number2)
        estimator = args.estimator
        if operator not in conf['types'].keys():
            raise TypeError('Operator must be one of: '+str(conf['types'].keys()))
        if estimator not in conf['estimators']:
            raise TypeError('Estimator must be one of: '+str(conf['estimators']))
        print(predict(number1, number2, operator, estimator))
        return 0
    except Exception as error:
        if type(error) == ValueError:
            error.args = ('Input (N1, N2) must be numbers',)
        print(error)
        return 1

if __name__ == '__main__':
    main()
