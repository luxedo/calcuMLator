#!/bin/env python2
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
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from matplotlib import cm
import data
import estimate

# data sets size
TRAINING_SIZE = 20
TRAINING_STEP = 3
TEST_SIZE = 10**3
TEST_RANGE = 2*10**3

# create training set
training_set = data.create_full_set(TRAINING_STEP, TRAINING_SIZE)
X_train, y_train_add, y_train_sub, y_train_mul, y_train_div = training_set

# create test set
test_set = data.create_random_set(TEST_RANGE, TEST_SIZE)
X_test, y_test_add, y_test_sub, y_test_mul, y_test_div = test_set


def plot_surface_function(function, rng, title=''):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    dat1 = np.logspace(-rng, rng, 20)
    # print(dat1)
    # dat1 = np.linspace(-5, 5, 30)
    X = Y = np.append(-np.flipud(dat1), dat1)
    X, Y = np.meshgrid(X, Y)
    Z = function(X, Y)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.magma, cstride=1, rstride=1,
                           vmin=-10, vmax=10, linewidth=0)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title(title)
    plt.show()


def plot_trisurface(xs, ys, zs, filename, title=''):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    # ax.set_zlim([-10, 10])
    surf0 = ax.plot_trisurf(xs, ys, zs, cmap=cm.magma, linewidth=0)
    # surf1 = ax.plot_trisurf(X_train[:,0], X_train[:,1], y_train_div, linewidth=0)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


def plot_dataset(sx, sy, title=''):
    plt.scatter(sx, sy, s=3)
    plt.title(title)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.show()


def make_graphs(estimator_name, estimator_title):
    res_add = [estimate.predict(i, j, '+', estimator_name) for i, j in X_test]
    plot_trisurface(X_test[:,0], X_test[:,1], res_add, 'docs/images/add_'+estimator_name+'.png', 'Test set - addition '+estimator_title)
    res_sub = [estimate.predict(i, j, '-', estimator_name) for i, j in X_test]
    plot_trisurface(X_test[:,0], X_test[:,1], res_sub, 'docs/images/sub_'+estimator_name+'.png', 'Test set - subtraction '+estimator_title)
    res_mul = [estimate.predict(i, j, '*', estimator_name) for i, j in X_test]
    plot_trisurface(X_test[:,0], X_test[:,1], res_mul, 'docs/images/mul_'+estimator_name+'.png', 'Test set - multiplication '+estimator_title)
    res_div = [estimate.predict(i, j, '/', estimator_name) for i, j in X_test]
    plot_trisurface(X_test[:,0], X_test[:,1], res_div, 'docs/images/div_'+estimator_name+'.png', 'Test set - division '+estimator_title)


if __name__ == '__main__':
    # # 2d plots
    # plot_dataset(X_test[:,0], X_test[:,1], 'Test set')
    # plot_dataset(X_train[:,0], X_train[:,1], 'Training set')
    #
    # # 3d plots
    # plot_trisurface(X_train[:,0], X_train[:,1], y_train_add, 'Training set addition')
    # plot_trisurface(X_test[:,0], X_test[:,1], y_test_add, 'Test set addition')
    # plot_trisurface(X_train[:,0], X_train[:,1], y_train_sub, 'Training set subtraction')
    # plot_trisurface(X_test[:,0], X_test[:,1], y_test_sub, 'Test set subtraction')
    # plot_trisurface(X_train[:,0], X_train[:,1], y_train_mul, 'Training set multiplication')
    # plot_trisurface(X_test[:,0], X_test[:,1], y_test_mul, 'Test set multiplication')
    # plot_trisurface(X_train[:,0], X_train[:,1], y_train_div, 'Training set division')
    # plot_trisurface(X_test[:,0], X_test[:,1], y_test_div, 'Test set division')

    estimator_name = 'SVR'
    estimator_title = 'Support Vectors'
    make_graphs(estimator_name, estimator_title)
