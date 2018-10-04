import tensorflow as tf
import json

from Functions import select_valid_wordids

result_path = '斗罗大陆/字数不大于10的词统计数据/至少出现10次的词中的前50.000000%的词统计数据/64维词向量.json'
with open(result_path) as f:
    data = json.load(f)
word_list = data['word_list']
word_vec_list = data['word_vec_list']
word_hits = data['word_hits']
dict_size = len(word_list)
word_vec_dim = len(word_vec_list[0])

#随机找valid_size个词计算他们之间的距离
valid_size = 1000  #验证用词的数量
valid_word_ids = select_valid_wordids(word_hits, valid_size)
word_vec_list = tf.constant(word_vec_list)
valid_vec = tf.nn.embedding_lookup(word_vec_list, valid_word_ids)  #找词向量
extended_validate = tf.tile(tf.reshape(valid_vec, [-1, word_vec_dim, 1]), [1, 1, valid_size])
diff = tf.transpose(extended_validate, [2, 1, 0]) - extended_validate  #把两个矩阵扩展并转置到维度匹配然后作差
distance = tf.sqrt(tf.reduce_sum(diff ** 2, 1))  #差的平方分别求和然后开方

with tf.Session() as sess:
    distances = sess.run(distance).transpose()
    nearst_ids = distances.argsort(axis=1)[:, 0:20].tolist()  #数组值从小到大的索引值然后取前20个
    for i, word_indexs in enumerate(nearst_ids):
        word_id = valid_word_ids[word_indexs[0]]  #在valid_word_ids表中找出单词实际的编号
        print('\n与命中%d次的词语“%s”距离最近的词：' %
              (word_hits[word_id], word_list[word_id]))
        for word_index in word_indexs:
            word_id = valid_word_ids[word_index]  #在valid_word_ids表中找出单词实际的编号
            print(word_list[word_id] + '\t\t' + str(distances[i, word_index]))
