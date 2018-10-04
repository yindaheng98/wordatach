import json
from sklearn.manifold import TSNE

from Functions import select_valid_wordids
from Functions import plot_with_words

result_path = '斗罗大陆/字数不大于10的词统计数据/至少出现10次的词中的前50.000000%的词统计数据/64维词向量.json'
valid_size = 1000
pic_path = '.'.join(result_path.split('.')[0:-1]) + '中%d个的分布图.png' % valid_size
with open(result_path) as f:
    data = json.load(f)
word_list = data['word_list']
word_vec_list = data['word_vec_list']
word_hits = data['word_hits']
valid_ids = select_valid_wordids(word_hits, valid_size)

valid_vecs = []
valid_words = []
for word_id in valid_ids:
    valid_vecs.append(word_vec_list[word_id])
    valid_words.append(word_list[word_id])
tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000, method='exact')
low_dim_vecs = tsne.fit_transform(valid_vecs)
#t_SNE聚类降维
plot_with_words(low_dim_vecs, valid_words, pic_path)
