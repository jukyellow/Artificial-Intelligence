# -*- coding: utf-8 -*-
"""keras-simple-seq2seq.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pmv_ZKl5KdEhZscPaNQUFTarpvVdv3QV
"""

# https://gist.github.com/rouseguy/1122811f2375064d009dac797d59bae9
import numpy as np
from keras.models import Sequential
from keras.layers import Activation, TimeDistributed, Dense, RepeatVector, LSTM
from keras.utils import np_utils
from keras.callbacks import TensorBoard
import os

# brew install graphviz
# pip3 install graphviz
# pip3 install pydot-ng
from keras.utils.vis_utils import plot_model

digit = "0123456789"
alpha = "abcdefghij"

char_set = list(set(digit + alpha))  # id -> char
char_dic = {w: i for i, w in enumerate(char_set)}

data_dim = len(char_set)  # one hot encoding size
seq_length = time_steps = 7
num_classes = len(char_set)

# Build training date set
dataX = []
dataY = []

for i in range(1000):
    rand_pick = np.random.choice(10, 7)
    x = [char_dic[digit[c]] for c in rand_pick]
    y = [char_dic[alpha[c]] for c in rand_pick]
    
    #x1 = [[digit[c]] for c in rand_pick]
    #y1 = [[alpha[c]] for c in rand_pick]
    #print("x: ", x1)
    #print("y: ", y1)
    #x:  [['5'], ['1'], ['2'], ['3'], ['5'], ['3'], ['6']]
    #y:  [['f'], ['b'], ['c'], ['d'], ['f'], ['d'], ['g']]
    
    dataX.append(x)
    dataY.append(y)
    
print(dataX)
print(dataY)

# One-hot encoding
dataX = np_utils.to_categorical(dataX, num_classes=num_classes)
# reshape X to be [samples, time steps, features]
dataX = np.reshape(dataX, (-1, seq_length, data_dim))

# One-hot encoding
dataY = np_utils.to_categorical(dataY, num_classes=num_classes)
# time steps
dataY = np.reshape(dataY, (-1, seq_length, data_dim))


print('Build model...')
TensorBoard(log_dir='./logs', histogram_freq=1,
            write_graph=True, write_images=False)

#print(dataX)
#print(dataY)

model = Sequential()
# "Encode" the input sequence using an RNN, producing an output of HIDDEN_SIZE
# note: in a situation where your input sequences have a variable length,
# use input_shape=(None, nb_feature).
model.add(LSTM(32, input_shape=(time_steps, data_dim), return_sequences=False))

# For the decoder's input, we repeat the encoded input for each time step
model.add(RepeatVector(time_steps))
# The decoder RNN could be multiple layers stacked or a single layer

model.add(LSTM(32, return_sequences=True))

# For each of step of the output sequence, decide which character should
# be chosen
model.add(TimeDistributed(Dense(data_dim)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.fit(dataX, dataY, epochs=100) #1000

__file__ = 'seq2seq_sample'
# Store model graph in png
# (Error occurs on in python interactive shell)
plot_model(model, to_file=os.path.basename(__file__) + '.png', show_shapes=True)

# Create test data set for fun
testX = []
testY = []
for i in range(10):
    rand_pick = np.random.choice(10, 7)
    x = [char_dic[digit[c]] for c in rand_pick]
    y = [alpha[c] for c in rand_pick]
    testX.append(x)
    testY.append(y)

print(testX)
print(testY)
    

# One-hot encoding
testX = np_utils.to_categorical(testX, num_classes=num_classes)
# reshape X to be [samples, time steps, features]
testX = np.reshape(testX, (-1, seq_length, data_dim))

predictions = model.predict(testX, verbose=0)
for i, prediction in enumerate(predictions):
    # print(prediction)
    x_index = np.argmax(testX[i], axis=1)
    x_str = [char_set[j] for j in x_index]

    index = np.argmax(prediction, axis=1)
    result = [char_set[j] for j in index]

    print(''.join(x_str), ' -> ', ''.join(result),
          " true: ", ''.join(testY[i]))