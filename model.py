"""
Catherine (Chaihyun) Lee & Lucy Newman (2018)
Contributions from Rick Stevens
"""

from generate_data import *
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os 
import time
import pickle

# Ignore tensorflow warning
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

class Model:

    def __init__(self, input_data, target_data):
        # Load input and target data
        self.input_data = input_data
        self.target_data = target_data

        # Run model
        self.run_model()

        # Optimize
        self.optimize()
 
    def run_model(self):
        conv1 = tf.layers.conv2d(inputs=self.input_data, filters=64, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
        self.output = tf.layers.dense(tf.layers.flatten(conv1), 1) + 65

 
    def optimize(self):
        # Calculae loss
        self.loss = tf.losses.mean_squared_error(self.target_data, self.output)
        self.train_op = tf.train.AdamOptimizer(0.001).minimize(self.loss)


def main(gpu_id = None):

    if gpu_id is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id

    # Reset Tensorflow graph
    tf.reset_default_graph()

    # Generate stimulus
    player = 3
    batch_size = 100

    # Placeholders for the tensorflow model
    x = tf.placeholder(tf.float32, shape=[batch_size,10,10,1])
    y = tf.placeholder(tf.float32, shape=[batch_size,1])
    
    # Model stats
    losses = []
    testing_losses = []

    config = tf.ConfigProto()
    with tf.Session(config=config) as sess:

        device = '/cpu:0' if gpu_id is None else '/gpu:0'
        with tf.device(device):
            model = Model(x,y)
        
        init = tf.global_variables_initializer()
        sess.run(init)

        # Train the model
        start = time.time()
        i = 0
        while True:
            # Generate training set
            raw_data, target_data = generate_train_batch(batch_size, player)
            input_data = raw_data.astype(np.bool).astype(np.float32)
            feed_dict = {x: input_data, y: target_data}
            _, train_loss, model_output = sess.run([model.train_op, model.loss, model.output], feed_dict=feed_dict)
            
            # Check current status
            if i % 10 == 0:
                # Print current status
                print('Player: {} | Iter: {} | Loss: {:8.3f} | Ouput: {} | Actual Moves: {}'.format(player, i,train_loss,model_output.mean(),target_data.mean()))
                losses.append(train_loss)
               
                # Plot loss curve
                if i > 0:
                    plt.plot(losses[1:])
                    plt.savefig('./run_training_curve.png')
                    plt.close()

                print(raw_data[np.argmin(model_output)][:,:,0])

            if i % 200 == 0:
                raw_data, target_data = generate_test_batch(batch_size, player)
                input_data = raw_data.astype(np.bool).astype(np.float32)
                feed_dict = {x: input_data, y: target_data}
                model_output = sess.run(model.output, feed_dict=feed_dict)

                best_board = raw_data[np.argmax(model_output)]
                np.save('./board_{}'.format(player),best_board)

            i += 1


if __name__ == "__main__":
    main()











# 