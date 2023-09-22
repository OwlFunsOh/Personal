"""
Writing machine code to guess the variables to
a linear equation
"""

#Target Equation: y = mx + b
#Input an x value, show a y value
#computer will guess what the m and b is

#Equation: y = 24x + 16

import tensorflow as tf
import numpy as np

#training data
x = np.array([5, 9, 14, 17, 26], dtype = int)
y = np.array([136, 232, 352, 424, 640], dtype = int)

#building a layer
l0 = tf.keras.layers.Dense(units=1, input_shape=[1])
model = tf.keras.Sequential([l0])

model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(0.1))

history = model.fit(x, y, epochs=10000, verbose=2)
print("Finished training the model")

#Predict value
print(model.predict([23]))

#Print what values the machine thinks we're missing
print("These are the layer variables: {}".format(l0.get_weights()))
