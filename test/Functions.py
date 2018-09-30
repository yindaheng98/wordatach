import matplotlib.pyplot as plt



def select_valid_wordids(word_list, word_count_maxs):
    """从word_list中读取指定数量的高频词用于验证，word_count_maxs[i]指示了要读多少个(i+1)字词"""
    valid_words = []  #读取的词表
    word_count = [0] * len(word_count_maxs)  #当前已读数目
    for i, word in enumerate(word_list):
        word_length = len(word)
        if word_count[word_length] < word_count_maxs[word_length]:  #如果这个词长的词没读够
            word_count[word_length] += 1
            valid_words.append(i)  #就接着读
    return valid_words



def plot_with_words(vecs_2dim, words, file):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(180, 180))  # in inches
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
