#!/bin/env python
'''
CalcuMLator data file

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

# data sets size
TRAINING_SIZE = 100
TRAINING_STEP = 3
TEST_SIZE = 1600
TEST_RANGE = 10**3

def create_random_set(size, maximum):
    '''
    Returns a set with the desired size
    '''
    X, y_add, y_sub, y_mul, y_div = [], [], [], [], []
    rand1 = [np.random.uniform(-size, size) for i in range(maximum)]
    rand2 = [np.random.uniform(-size, size) for i in range(maximum)]
    for a, b in zip(rand1, rand2):
        X.append([a, b])
        y_add.append(np.add(a, b))
        y_sub.append(np.subtract(a, b))
        y_mul.append(np.multiply(a, b))
        y_div.append(np.divide(a, b))
    return np.array(X), np.array(y_add), np.array(y_sub), np.array(y_mul), np.array(y_div)

def create_full_set(step, maximum):
    '''
    Returns a grid set with up to the "maximum" value and with "step" spacing
    '''
    X, y_add, y_sub, y_mul, y_div = [], [], [], [], []
    dat1 = np.logspace(-1, step, )
    x0 = np.append(-np.flipud(dat1), dat1)
    for i in x0:
        for j in x0:
            if j == 0:
                continue
            X.append([i, j])
            y_add.append(np.add(i, j))
            y_sub.append(np.subtract(i, j))
            y_mul.append(np.multiply(i, j))
            y_div.append(np.divide(i, j))
    return np.array(X), np.array(y_add), np.array(y_sub), np.array(y_mul), np.array(y_div)

# create training set
X_train, y_train_add, y_train_sub, y_train_mul, y_train_div= create_full_set(TRAINING_STEP, TRAINING_SIZE)

# create test set
X_test, y_test_add, y_test_sub, y_test_mul, y_test_div = create_random_set(TEST_RANGE, TEST_SIZE)
print(X_train.shape)
