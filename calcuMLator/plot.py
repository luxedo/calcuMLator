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
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from data import *

def fun(x, y):
  return x+y

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
x = np.arange(-10.0, 10.0, 0.5)
y = x[x!=0]
X, Y = np.meshgrid(x, y)
zs = np.array([fun(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])

# x, y = X_train[:,0], X_train[:,1]
# X, Y = np.meshgrid(x, y)
# zs = y_train_add
# zs = np.array(oi)
Z = zs.reshape(X.shape)

# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.magma, linewidth=0, vmin=-5,
# vmax=5)
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.magma, linewidth=0)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()

def plot_dataset(datax, datay):
    plt.scatter(datax, datay)
    plt.title('Test set')
    plt.ylabel('y')
    plt.xlabel('x')
    plt.show()

dat1 = np.logspace(0, 1.5, 20)-1
dat = np.append(-np.flipud(dat1), dat1)
meshx, meshy = np.meshgrid(dat, dat)
# plot_dataset(dat, dat)

dat1 = [np.random.uniform(-100, 100) for i in range(1600)]
dat2 = [np.random.uniform(-100, 100) for i in range(1600)]
plot_dataset(dat1, dat2)
