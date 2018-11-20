"""
Catherine (Chaihyun) Lee & Lucy Newman (2018)
Contributions from Rick Stevens
"""

import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os 
import time

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

        # x = tf.reshape(self.input_data, shape=[par['batch_train_size'],*par['inp_img_shape'],1])
        conv1 = tf.layers.conv2d(inputs=self.input_data, filters=64, kernel_size=(3,3), padding='same', activation=tf.nn.relu)
        self.output = tf.layers.dense(tf.layers.flatten(conv1), 1, activation=tf.nn.relu)

 
    def optimize(self):
        # Calculae loss
        print(self.target_data.shape)
        print(self.output.shape)
        self.loss = tf.losses.mean_squared_error(self.target_data, self.output)
        self.train_op = tf.train.AdamOptimizer(0.0001).minimize(self.loss)

def generate_train_batch(batch_size):
    input_data = np.random.randint(2,size=(batch_size,10,10,1))
    target_data = np.random.randint(2,size=(batch_size,1))
    return input_data, target_data

def main(gpu_id = None):

    if gpu_id is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id

    # Reset Tensorflow graph
    tf.reset_default_graph()

    # Generate stimulus
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
        for i in range(1000):

            # Generate training set
            input_data, target_data = generate_train_batch(batch_size)
            feed_dict = {x: input_data, y: target_data}
            _, train_loss, model_output = sess.run([model.train_op, model.loss, model.output], feed_dict=feed_dict)
            
            # Check current status
            if i % 10 == 0:

                # Print current status
                # print('Model {:2} | Task: {:s} | Iter: {:6} | Loss: {:8.3f} | Run Time: {:5.3f}s'.format( \
                    # 1, 1, i, train_loss, time.time()-start))
                losses.append(train_loss)
               
                # Plot loss curve
                if i > 0:
                    plt.plot(losses[1:])
                    plt.savefig('./run_training_curve.png')
                    plt.close()



if __name__ == "__main__":
    main()











# 