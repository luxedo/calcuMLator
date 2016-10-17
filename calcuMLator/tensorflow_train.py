#!/bin/env python
'''
CalcuMLator TensorFlow training file

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
import tensorflow as tf
import numpy as np
from os import path
import json
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
training_set = data.create_random_set(TEST_RANGE, TEST_SIZE)
X_train, y_train_add, y_train_sub, y_train_mul, y_train_div = training_set

# create training set
validation_set = data.create_random_set(TEST_RANGE, TEST_SIZE)
X_val, y_val_add, y_val_sub, y_val_mul, y_val_div = validation_set

# create test set
test_set = data.create_random_set(TEST_RANGE, TEST_SIZE)
X_test, y_test_add, y_test_sub, y_test_mul, y_test_div = test_set

def model(X, w_linear, b_linear, w_hidden, b_hidden):
    '''
    Predictor model for the neural network
    '''
    X_hidden = tf.nn.bias_add(tf.matmul(X, w_hidden), b_hidden)
    Y = tf.nn.bias_add(tf.matmul(X_hidden, w_linear), b_linear)
    return Y

def accuracy(predictions, labels):
  return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
          / predictions.shape[0])

def r2_score(predictions, labels):
    '''
    Returns the r2 score for the predictions
    '''
    y_mean = tf.reduce_mean(labels)
    SSres = tf.reduce_sum(tf.square(labels-predictions))
    SStot = tf.reduce_sum(tf.square(labels-y_mean))
    r2 = 1 - SSres/SStot
    return r2

def train_tensorflow(X_train, y_train, X_val, y_val, X_test, y_test):
    '''
    Creates the linear regression estimator and returns it along with it's r2_score
    '''
    hidden_size = 100
    graph = tf.Graph()

    X_train = tf.constant(X_train, dtype=tf.float32)
    y_train = tf.constant(y_train, dtype=tf.float32)

    X_val = tf.constant(X_val, dtype=tf.float32)
    y_val = tf.constant(y_val, dtype=tf.float32)

    X_test = tf.constant(X_test, dtype=tf.float32)
    y_test = tf.constant(y_test, dtype=tf.float32)

    w_hidden = tf.Variable(tf.truncated_normal([2, hidden_size]))
    b_hidden = tf.Variable(tf.zeros([hidden_size]))

    w_linear = tf.Variable(tf.truncated_normal([hidden_size, 1]))
    b_linear = tf.Variable(tf.zeros([1]))

    hidden = tf.nn.softplus(tf.nn.bias_add(tf.matmul(X_train, w_hidden), b_hidden))
    logits = tf.nn.bias_add(tf.matmul(hidden, w_linear), b_linear)

    train_pred = model(X_train, w_linear, b_linear, w_hidden, b_hidden)
    val_pred = model(X_val, w_linear, b_linear, w_hidden, b_hidden)
    test_pred = model(X_test, w_linear, b_linear, w_hidden, b_hidden)
    loss = tf.reduce_mean(tf.square(train_pred - y_train))

    train_op = tf.train.GradientDescentOptimizer(2*10**-8).minimize(loss)

    with tf.Session() as sess:
        tf.initialize_all_variables().run()

        for step in range(30):
            # _, l, predictions = sess.run([train_op, loss, y_train])
            # if step%50 == 0:
                # print('Loss at step {0}: {1}'.format(step, l))
            # print(predictions[0])

            _, l, predictions = sess.run([train_op, loss, y_train])
            # print(r2_score(Y_test, y_test).eval())
            # print(Y_test.eval()[:3], y_test[:3].eval())
            print(train_pred.eval()[:1], y_train.eval()[:1])
            # print(test_pred.eval()[:1], y_test.eval()[:1])

        # print(y_train_mul[0])
        # print((X_train[0: 3, :].eval()))
        # print(y_train_div[0: 3])
        # print(model(X_train[0: 3, :], w_linear, b_linear, w_hidden, b_hidden).eval())
        # print(predictions[0: 3])
        # print(predictions[0:3])
        # print(y_train_add[0:3])
        # print(l)
        # print(l)


if __name__ == '__main__':
    train_tensorflow(X_train, y_train_add, X_val, y_val_add, X_test, y_test_add)
    # train_tensorflow(X_train, y_train_mul, X_val, y_val_mul, X_test, y_test_mul)
    # train_tensorflow(X_train, y_train_div, X_val, y_val_mul, X_test, y_test_div)
