'''
This program will try to get a machine to learn how to calulate celsius
Playing around with code from udacity
'''

import tensorflow as tf
import numpy as np
import logging
import matplotlib.pyplot as plt



#below gets a logger from tensorflow
logger = tf.get_logger()

"""
The five levels of logging from most severe to least is:
FATAL/CRITICAL
ERROR
WARN
INFO
DEBUG

We want to set it so it shows errors and fatal
"""

logger.setLevel(logging.ERROR)

#training data
fahrenheit_a = np.array([-40,  14, 32, 46, 59, 72, 100],  dtype=float)
celsius_q    = np.array([-40, -10,  0,  8, 15, 22,  38],  dtype=float)

#building a layer
l0 = tf.keras.layers.Dense(units=1, input_shape=[1])
model = tf.keras.Sequential([l0])

#compiling
#Loss: how far predictions are from outcome
#Optimizer: adjusting values to reduce loss. Usually between 0.001 and 0.1
#My guess for now is optimizer is how much you want to change the value by when guessing?

model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(0.1))
history = model.fit(fahrenheit_a, celsius_q, epochs=10000, verbose=False)
print("Finished training the model")

#Predict value
print(model.predict([46.0]))

#Print what values the machine thinks we're missing
print("These are the layer variables: {}".format(l0.get_weights()))