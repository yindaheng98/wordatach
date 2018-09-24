#coding=utf-8
import json
import os

from wordatas.BuildDict import BuildDict



class DataInput:
    word_dict = {}  #编号-单词词典
    tree_dict = {}  #树形词典
    word_data = ''  #预处理数据文件


    def __init__(self, path, wordn_max, feq_min, count_percent):
        #数据文件路径
        index_path = path.split('.')[0] + '\\'
        #原文存储路径
        word_data_path = index_path + 'word_data.json'
        #词频存储路径
        word_counts_path = index_path + 'word_counts_%d.json' % wordn_max
        #词典存储路径
        word_dict_path = index_path + 'word_dict_%d_%d_%f.json' % (wordn_max, feq_min, count_percent)
        #树形词典存储路径
        tree_dict_path = index_path + 'tree_dict_%d_%d_%f.json' % (wordn_max, feq_min, count_percent)
        #读取原文
        if not os.path.exists(index_path):
            os.makedirs(index_path)  #没有路径先创建路径
        #读取或构建词典
        if os.path.exists(tree_dict_path):  #如果有树形词典文件存在
            with open(tree_dict_path, 'r', encoding='utf-8') as f:  #就直接读取树形词典
                tree_dict = json.load(f)
        else:
            if os.path.exists(word_dict_path):  #如果有词典文件存在
                with open(word_dict_path, 'r', encoding='utf-8') as f:  #就直接读取词典
                    word_dict = json.load(f)
            else:  #如果没有词典文件
                if os.path.exists(word_counts_path):  #但有词频文件
                    with open(word_counts_path, 'r', encoding='utf-8') as f:  #就直接读取词频
                        word_counts = json.load(f)
                else:  #如果没有词频文件
                    if os.path.exists(word_data_path):  #但有原数据文件
                        word_data = BuildDict.read_origional_file(word_data_path)  #就读取原数据文件
                    else:
                        word_data = BuildDict.read_origional_file(path)  #构建原数据
                        with open(word_data_path, 'w', encoding='utf-8') as f:  #记录原数据文件
                            f.writelines(word_data)
                    word_counts = BuildDict.count_words(word_data, wordn_max)  #构建词频
                    with open(word_counts_path, 'w', encoding='utf-8') as f:  #记录词频文件
                        json.dump(word_counts, f)
                word_dict = BuildDict.build_dict_from_counts(word_counts, feq_min, count_percent)  #构建词典
                with open(word_dict_path, 'w', encoding='utf-8') as f:  #记录词典文件
                    json.dump(word_dict, f)
            tree_dict = BuildDict.convert_tree_dict(word_dict)
            with open(tree_dict_path, 'w', encoding='utf-8') as f:  #记录树形词典文件
                json.dump(tree_dict, f)
        self.tree_dict = tree_dict  #树形词典文件进入内存
        with open(word_dict_path, 'r', encoding='utf-8') as f:  #记录词典文件
            self.word_dict = json.load(f)  #编号-单词词典文件进入内存
        self.wordn_max = wordn_max
        self.word_data = open(word_data_path, 'r', encoding='utf-8')  #打开原数据文件
        self.words = []
        self.__update_words()


    def data_reload(self, word_data_path):
        """重新载入数据文件,用于在生成词典之后切换其他源文件"""
        self.word_data.close()
        self.word_data = open(word_data_path, 'r', encoding='utf-8')  #打开原数据文件
        self.words = []
        self.__update_words()


    wordn_max = 0  #最大子长
    words = []  #要检测的一串字


    def __update_words(self):
        """更新last_w使长度达到wordn_max字"""
        needs = self.wordn_max - len(self.words)  #算出缺少多少字达到wordn_max字
        for _ in range(0, needs):
            self.words.append(self.word_data.read(1))  #并读入一串字


    def __next_word(self):
        """从文本中切出一个单词"""
        self.__update_words()  #先补齐words
        has_id = []
        next_word = 0
        r = self.tree_dict  #开始树形搜索,r表示树形搜索当前到达的范围
        for i in range(0, self.wordn_max):
            word = self.words[i]  #读入1个字
            if word in r:  #如果r的分支内有这个字
                r = r[word]  #进入下分支
                has_id.append('id' in r)  #记录这个分支里面是否有id
            else:  #如果r的分支内没有这个字说明搜索到达所要节点
                if 'id' in r:  #如果这个叶节点有id说明找到了所要的词
                    next_word = r['id']  #那么返回的词就是当前词
                    self.words = self.words[i if not i == 0 else 1:]  #然后把已检索到的词删掉,如果一个词都没检索到就滑动一格
                else:  #如果r域没有id说明不是终点而且要回溯
                    layer = 0
                    for layer in range(0, len(has_id)):
                        if not has_id[layer]:
                            break
                    #通过has_id回溯上一个有id的主枝层数layer
                    r = self.tree_dict
                    for j in range(0, layer):
                        r = r[self.words[j]]
                    next_word = r['id']  #返回最近的有id词语
                    self.words = self.words[layer if not layer == 0 else 1:]  #然后把已检索到的词删掉
                break
        #return self.word_dict[str(next_word)] if not next_word == 0 else next_word
        return next_word


    last_word = ''  #记录上一个词


    def __next_batch(self):
        """下一个训练对"""
        next_word = self.__next_word()  #读入wordn_max位
        batch = (self.last_word, next_word)
        self.last_word = next_word
        return batch


    def next_batchs(self, n):
        """读出n个训练对"""
        batches = []
        for _ in range(0, n):
            batches.append(self.__next_batch())
        return batches
