import tensorflow as tf
import json
import numpy as np

valid_size = 16  #验证用词的数量
result_path = '斗罗大陆\字数不大于10且至少出现10次的词中的前50.000000%的result.json'
with open(result_path) as f:
    data = json.load(f)
word_list = data['word_list']
word_vec_list = data['word_vec_list']
dict_size = len(word_list)
word_vec_dim = len(word_vec_list[0])
#随机找16个词计算他们与所有词汇之间的距离
word_vec_list = tf.constant(word_vec_list)
valid_words = tf.random_uniform(shape=[valid_size], minval=1, maxval=dict_size, dtype=tf.int32)
valid_vecs = tf.nn.embedding_lookup(word_vec_list, valid_words)  #找词向量
extended_validate = tf.tile(tf.reshape(valid_vecs, [-1, word_vec_dim, 1]), [1, 1, dict_size])
extended_worddict = tf.tile(tf.reshape(word_vec_list, [-1, word_vec_dim, 1]), [1, 1, valid_size])
diff = tf.transpose(extended_validate, [2, 1, 0]) - extended_worddict  #把两个矩阵扩展并转置到维度匹配然后作差
distance = tf.sqrt(tf.reduce_sum(diff ** 2, 1))  #差的平方分别求和然后开方

with tf.Session() as sess:
    distances = sess.run(distance).transpose()
    nearst_ids = distances.argsort(axis=1)[:, 0:20].tolist()  #数组值从小到大的索引值然后取前20个
    i = 0
    for word_ids in nearst_ids:
        print('与词语“%s”距离最近的词：\n' % word_list[word_ids[0]])
        for word_id in word_ids:
            print(word_list[word_id]+'\t\t'+str(distances[i, word_id]))
        i += 1
