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
from sklearn.externals import joblib
import os.path
import argparse

FOLDER = os.path.dirname(__file__)+'/estimators/'
LINEAR_ADD_ESTIMATOR_PATH = FOLDER + 'linear_add_estimator.pkl'
LINEAR_MUL_ESTIMATOR_PATH = FOLDER + 'linear_mul_estimator.pkl'

SVC_ADD_ESTIMATOR_PATH = FOLDER + 'SVC_add_estimator.pkl'
SVC_MUL_ESTIMATOR_PATH = FOLDER + 'SVC_mul_estimator.pkl'

NN_ADD_ESTIMATOR_PATH = FOLDER + 'NN_add_estimator.pkl'
NN_MUL_ESTIMATOR_PATH = FOLDER + 'NN_mul_estimator.pkl'

def predict(number1, number2, operator, brain):
    '''
    Predicts the value of the operation
    '''
    if brain == 'linear':
        clf_add = joblib.load(LINEAR_ADD_ESTIMATOR_PATH)
    elif brain == 'SVC':
        clf_add = joblib.load(SVC_ADD_ESTIMATOR_PATH)
    elif brain == 'NN':
        clf_add = joblib.load(NN_ADD_ESTIMATOR_PATH)
    if operator == '+':
        return clf_add.predict([number1, number2])[0]
    elif operator == '-':
        return clf_add.predict([number1, -number2])[0]
    elif operator == '*':
        acc = 0
        for i in range(int(number1)):
            acc =  clf_add.predict([acc, number2])
        acc += number1%1*number2
        return acc
    elif operator == '/':
        acc = 0
        while number1-number2 > 0:
            acc += 1
            number1 = clf_add.predict([number1, -number2])
        acc += number1/number2
        return acc

def main():
    parser = argparse.ArgumentParser(description='Calculates the operation using Machine Learning')
    parser.add_argument('number1', metavar='N1', help='a number for the calculation')
    parser.add_argument('operator', metavar='OP', help='The operator for the calculation (+, -, *, /)')
    parser.add_argument('number2', metavar='N2', help='a number for the calculation')
    parser.add_argument('brain', metavar='B', help='The brain for the calculation (linear, SVC, NN)')

    args = parser.parse_args()

    try:
        number1 = float(args.number1)
        operator = args.operator
        number2 = float(args.number2)
        brain = args.brain
        if operator not in ('+', '-', '*', '/'):
            raise TypeError('Operator must be one of: +, -, *, /')
        if brain not in ('linear', 'SVC', 'NN'):
            raise TypeError('Brain must be one of: linear, SVC, NN')
        print(predict(number1, number2, operator, brain))
        return 0
    except Exception as error:
        if type(error) == ValueError:
            error.args = ('Input (N1, N2) must be numbers',)
        print(error)
        return 1

if __name__ == '__main__':
    main()
