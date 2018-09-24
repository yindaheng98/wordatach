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
        self.last_w = self.word_data.read(1)  #并读入一个字


    def data_reload(self, word_data_path):
        """重新载入数据文件,用于在生成词典之后切换其他源文件"""
        self.word_data.close()
        self.word_data = open(word_data_path, 'r', encoding='utf-8')  #打开原数据文件
        self.last_w = self.word_data.read(1)  #并读入一个字


    wordn_max = 0  #最大子长
    last_w = ''  #上一个字


    def __next_word(self):
        """从文本中切出一个单词"""
        next_word = 0  #如果没有在根节点找到字就返回0
        if self.last_w in self.tree_dict:  #如果上一个词在树形词典根节点中
            r = self.tree_dict[self.last_w]  #开始树形搜索,r表示树形搜索当前到达的范围
            for _ in range(0, self.wordn_max):
                next_w = self.word_data.read(1)  #读入1个字
                if next_w in r:  #如果此范围内有这个字
                    r = r[next_w]  #进入下一层
                else:  #如果此范围内没有这个字说明搜索到达终点
                    next_word = r['id']  #那么下一个词就是当前域对应的词
                    self.last_w = next_w  #然后把这个字作为上一字
                    break
        else:  #否则如果根节点没有
            self.last_w = self.word_data.read(1)  #就后移一位
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
