import tensorflow as tf
import json

from Functions import select_valid_wordids

result_path = '斗罗大陆\字数不大于10且至少出现10次的词中的前50.000000%的result.json'
with open(result_path) as f:
    data = json.load(f)
word_list = data['word_list']
word_vec_list = data['word_vec_list']
dict_size = len(word_list)
word_vec_dim = len(word_vec_list[0])

'''
valid_size = 16  #验证用词的数量
valid_wordids = tf.random_uniform(dtype=tf.int32, shape=[valid_size], minval=1, maxval=dict_size)
'''
valid_wordids = select_valid_wordids(word_list, [0, 100, 50, 25, 25, 0, 0, 0, 0, 0])
valid_size = len(valid_wordids)  #验证用词的数量
valid_wordids = tf.constant(valid_wordids)
#随机找16个词计算他们与所有词汇之间的距离
word_vec_list = tf.constant(word_vec_list)
valid_vec = tf.nn.embedding_lookup(word_vec_list, valid_wordids)  #找词向量
extended_validate = tf.tile(tf.reshape(valid_vec, [-1, word_vec_dim, 1]), [1, 1, dict_size])
extended_worddict = tf.tile(tf.reshape(word_vec_list, [-1, word_vec_dim, 1]), [1, 1, valid_size])
diff = tf.transpose(extended_validate, [2, 1, 0]) - extended_worddict  #把两个矩阵扩展并转置到维度匹配然后作差
distance = tf.sqrt(tf.reduce_sum(diff ** 2, 1))  #差的平方分别求和然后开方

with tf.Session() as sess:
    distances = sess.run(distance).transpose()
    nearst_ids = distances.argsort(axis=1)[:, 0:20].tolist()  #数组值从小到大的索引值然后取前20个
    i = 0
    for word_ids in nearst_ids:
        print('\n与词语“%s”距离最近的词：' % word_list[word_ids[0]])
        for word_id in word_ids:
            print(word_list[word_id] + '\t\t' + str(distances[i, word_id]))
        i += 1


