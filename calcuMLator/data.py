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
RANGE = 4

# training and test sets
X_train,  X_test = [], []
y_train_add, y_test_add = [], []
y_train_mul, y_test_mul = [], []
# y_train_sub, y_test_sub = [], []
# y_train_div, y_test_div = [], []

for i in range(RANGE):
    for j in range(RANGE):
        a = np.random.randint(10*RANGE)
        b = np.random.randint(10*RANGE)

        X_train.append([a, b])

        y_train_add.append(np.add(a, b))
        y_train_mul.append(np.multiply(a, b))
        # y_train_sub.append(np.subtract(a, b))
        # y_train_div.append(np.divide(a, b))

        a = np.random.randint(10*RANGE)
        b = np.random.randint(10*RANGE)

        X_test.append([a, b])

        y_test_add.append(np.add(a, b))
        y_test_mul.append(np.multiply(a, b))
        # y_test_sub.append(np.subtract(a, b))
        # y_test_div.append(np.divide(a, b))
