from wordatas.DataInput import DataInput
import numpy as np
import tensorflow as tf
import numpy.random as random

data_input = DataInput('斗罗大陆.txt', 10, 10, 0.5)
print(data_input.next_batch_for_RNN(32, 8))
print(data_input.next_batch_for_RNN(32, 8))
print(data_input.next_batch_for_RNN(32, 8))
print(data_input.next_batches_for_cbow(30))
print(data_input.next_batches_for_cbow(10))
print(data_input.next_batches_for_cbow(10))
print(data_input.next_batches_for_skipgram(32))
print(data_input.next_batches_for_skipgram(30))
print(data_input.next_batches_for_skipgram(10))
'''
batches = data_input.next_batches_for_skipgram(10)
batches = np.array(batches)
inputs = batches[:, 0].reshape(1, -1)
outputs = batches[:, 1]
data_input.word_data.close()
a = tf.constant(random.rand(10, 3))
b = tf.constant(random.rand(20, 3))
ra = tf.reshape(a, [-1, 3, 1])
rb = tf.reshape(b, [-1, 3, 1])
tra = tf.tile(ra, [1, 1, 20])
trb = tf.tile(rb, [1, 1, 10])
cc = trb - tf.transpose(tra, [2, 1, 0])
with tf.Session() as sess:
    print(sess.run(cc))
'''
'''
#Here is the bug,watch the variable t and see what will happen
f = open('斗罗大陆/word_data.json', 'r', encoding='utf-8')
while 1:
    f.seek(34)
    fp=f.tell()
    t=f.read(11)
    fp=f.tell()
    fp
f = open('斗罗大陆/word_data.json', 'r', encoding='utf-8')
while 1:
    f.seek(0)
    fp=f.tell()
    t=f.read(12)
    fp=f.tell()
    t = f.seek(18446744073709551650)
    t = f.read(12)
    fp
'''
