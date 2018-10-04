import matplotlib.pyplot as plt
import numpy as np



def select_valid_wordids(word_hits, word_count_maxs):
    """从word_list中读取命中次数排前word_count_maxs的词语用于验证"""
    return np.argsort(a=-np.array(word_hits), axis=0)[1:word_count_maxs + 1].tolist()



def plot_with_words(vecs_2dim, words, file):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(24, 24))  # in inches
    for i, label in enumerate(words):
        x, y = vecs_2dim[i, :]
        plt.scatter(x, y)
        plt.annotate(
            label,
            xy=(x, y),
            xytext=(5, 2),
            textcoords='offset points',
            ha='right',
            va='bottom')
    plt.savefig(file)
