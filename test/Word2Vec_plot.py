import json
from sklearn.manifold import TSNE

from Functions import select_valid_wordids
from Functions import plot_with_words

result_path = '斗罗大陆\字数不大于10且至少出现10次的词中的前50.000000%的result.json'
with open(result_path) as f:
    data = json.load(f)
word_list = data['word_list']
word_vec_list = data['word_vec_list']
valid_ids = select_valid_wordids(word_list, [0, 1000, 500, 250, 250, 100, 100, 100, 100, 100])

valid_vecs = []
valid_words = []
for word_id in valid_ids:
    valid_vecs.append(word_vec_list[word_id])
    valid_words.append(word_list[word_id])
tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000, method='exact')
low_dim_vecs = tsne.fit_transform(valid_vecs)
#t_SNE聚类降维
plot_with_words(low_dim_vecs, valid_words, '斗罗大陆\字数不大于10且至少出现10次的词中的前50.000000%的result.png')
