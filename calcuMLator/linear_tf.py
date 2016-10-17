#!/usr/bin/env python

import tensorflow as tf
import numpy as np
import data

SIZE = 10**3
MAXIMUM = 20**3

trX, trY_add, trY_sub, trY_mul, trY_div = data.create_random_set(SIZE, MAXIMUM)
teX, teY_add, teY_sub, teY_mul, teY_div = data.create_random_set(SIZE, MAXIMUM)
trY_add = [np.transpose(trY_add)]

hidden_size = 20
learning_rate = 0.5
num_steps = 3001


def model(X, w_linear, b_linear, w_hidden, b_hidden):
    '''
    Predictor model for the neural network
    '''
    X_hidden = tf.nn.relu(tf.nn.bias_add(tf.matmul(X, w_hidden), b_hidden))
    Y = tf.nn.bias_add(tf.matmul(X_hidden, w_linear), b_linear)
    return Y

graph = tf.Graph()
with graph.as_default():

    # Input data. For the training data, we use a placeholder that will be fed
    # at run time with a training minibatch.
    tf_train_dataset = tf.placeholder(tf.float32, shape=(len(trX), 2))
    tf_train_labels = tf.placeholder(tf.float32, shape=(len(trX), 1))
    # tf_valid_dataset = tf.constant(valid_dataset)
    tf_test_dataset = tf.constant(teX, tf.float32)

    # Variables.
    weights = tf.Variable(tf.truncated_normal([hidden_size, 1]), tf.float32)
    biases = tf.Variable(tf.zeros([1]))
    weights_nn = tf.Variable(tf.truncated_normal([2, hidden_size]))
    biases_nn = tf.Variable(tf.truncated_normal([hidden_size]))

    # Training computation.
    pred = model(tf_train_dataset, weights, biases, weights_nn, biases_nn)
    loss = tf.reduce_sum(tf.pow(pred-tf_train_labels, 2))/(2*len(trX)) # Softmax loss
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(loss)

    # Predictions for the training, validation, and test data.
    train_prediction = pred
    test_prediction = model(tf_test_dataset, weights, biases, weights_nn, biases_nn)


with tf.Session(graph=graph) as session:
    tf.initialize_all_variables().run()
    print("Initialized")
    for step in range(num_steps):
        feed_dict = {tf_train_dataset: trX, tf_train_labels: trY_add}
        _, l, predictions = session.run(
        [optimizer, loss, train_prediction], feed_dict=feed_dict)
        # if (step % 500 == 0):
            # print("Batch loss at step %d: %f" % (step, l))
            # print("Batch accuracy: %.1f%%" % accuracy(predictions, trY_add))
            # print("Validation accuracy: %.1f%%" % accuracy(
                # valid_prediction.eval(), valid_labels))
    # print("Test accuracy: %.1f%%" % accuracy(test_prediction.eval(), test_labels))
