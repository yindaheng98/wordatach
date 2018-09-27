import tensorflow as tf
from wordatas.DataInput import DataInput
import math
import numpy as np

data_input = DataInput('斗罗大陆.txt', 10, 10, 0.5)

#初始化输入数据
batch_size = 128  #每次的样本数量
nega_batch_size = 64  #每次的负样本数量
word_vec_dim = 3  #词向量的维度
dict_size = data_input.dict_size  #单词数量

with tf.name_scope('training_batch'):  #训练样本的placeholder
    train_input = tf.placeholder(dtype=tf.int32, shape=[batch_size], name='train_input')  #行向量输入
    train_label = tf.placeholder(dtype=tf.int32, shape=[batch_size, 1], name='train_output')  #列向量输出

with tf.name_scope('vector_list'):  #词嵌入矩阵及查找操作
    word_vec_list = tf.Variable(dtype=tf.float32,
                                initial_value=tf.random_uniform(shape=[dict_size, word_vec_dim],
                                                                minval=-1.0,
                                                                maxval=1.0))
    input_word_vecs = tf.nn.embedding_lookup(word_vec_list, train_input)

with tf.name_scope('NCE_loss'):  #NCE loss
    nce_weight = tf.Variable(dtype=tf.float32,
                             initial_value=tf.truncated_normal(shape=[dict_size, word_vec_dim],
                                                               stddev=1.0 / math.sqrt(word_vec_dim)))
    nce_bias = tf.Variable(dtype=tf.float32,
                           initial_value=tf.zeros(shape=[dict_size]))
    nce_loss = tf.nn.nce_loss(weights=nce_weight,
                              biases=nce_bias,
                              inputs=input_word_vecs,
                              labels=train_label,
                              num_sampled=nega_batch_size,
                              num_classes=dict_size)

with tf.name_scope('loss_and_optimizer'):  #总loss和优化操作
    loss = tf.reduce_mean(nce_loss)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0).minimize(loss)

saver = tf.train.Saver()

#tensorboard记录
tf.summary.scalar('loss', loss)
merge = tf.summary.merge_all()

with tf.Session() as sess:
    writer = tf.summary.FileWriter('word2vec_log', sess.graph)
    sess.run(tf.global_variables_initializer())
    for step in range(1000000):
        try:
            batches = np.array(data_input.next_batches_for_skipgram(batch_size))
        except IOError:
            break
        inputs = batches[:, 0]
        labels = batches[:, 1].reshape(-1, 1)
        feed_dict = {train_input: inputs, train_label: labels}
        _, summary = sess.run([optimizer, merge], feed_dict=feed_dict)
        writer.add_summary(summary, step)
    data_input.record_result(sess.run(word_vec_list).tolist())
    saver.save(sess, 'word2vec_log/model.ckpt')
    writer.close()
data_input.word_data.close()
