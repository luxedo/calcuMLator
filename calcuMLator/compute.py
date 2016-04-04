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
ADD_ESTIMATOR_PATH = FOLDER + 'add_estimator.pkl'
MUL_ESTIMATOR_PATH = FOLDER + 'mul_estimator.pkl'

def predict(number1, number2, operator):
    '''
    Predicts the value of the operation
    '''
    clf_add = joblib.load(ADD_ESTIMATOR_PATH)
    if operator == '+':
        return clf_add.predict([number1, number2])[0]
    elif operator == '-':
        return clf_add.predict([number1, -number2])[0]
    elif operator == '*':
        return sum([clf_add.predict([number2, number2])]*number1)[0]
    elif operator == '/':
        return 12

def main():
    parser = argparse.ArgumentParser(description='Calculates the operation using Machine Learning')
    parser.add_argument('number1', metavar='N1', help='a number for the calculation')
    parser.add_argument('operator', metavar='OP', help='The operator for the calculation (+, -, *, /)')
    parser.add_argument('number2', metavar='N2', help='a number for the calculation')

    args = parser.parse_args()

    try:
        number1 = float(args.number1)
        operator = args.operator
        number2 = float(args.number2)
        if operator not in ('+', '-', '*', '/'):
            raise TypeError('Operator must be one of: +, -, *, /')
        print(predict(number1, number2, operator))
        return 0
    except Exception as error:
        if type(error) == ValueError:
            error.args = ('Input (N1, N2) must be numbers',)
        print(error)
        return 1

if __name__ == '__main__':
    main()
