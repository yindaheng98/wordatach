#coding=utf-8
import json
import os

from wordatas.BuildDict import BuildDict



class DataInput:
    word_dict = {}  #词典
    word_data = ''  #预处理数据文件
    wordn_max = 0


    def __init__(self, path, wordn_max, feq_min, count_percent):
        #数据文件路径
        index_path = path.split('.')[0] + '\\'
        #原文存储路径
        word_data_path = index_path + 'word_data.json'
        #词频存储路径
        word_counts_path = index_path + 'word_counts_%d.json' % wordn_max
        #词典存储路径
        word_dict_path = index_path + 'word_dict_%d_%d_%f.json' % (wordn_max, feq_min, count_percent)
        #读取原文
        if not os.path.exists(index_path):
            os.makedirs(index_path)  #没有路径先创建路径
        #读取或构建词典
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
        self.word_dict = word_dict
        self.word_data = open(word_data_path, 'r', encoding='utf-8')  #打开原数据文件
        self.wordn_max = wordn_max


    def data_reload(self, word_data_path):
        '''重新载入数据文件,用于在生成词典之后载入其他源文件'''
        self.word_data.close()
        self.word_data = open(word_data_path, 'r', encoding='utf-8')


    @staticmethod
    def __utf8width(text, n):  #统计最后n个字符的位宽
        return len(text[len(text) - n:].encode('utf-8'))


    def __next_word(self):
        '''找到下一个单词'''
        next_wordmax = self.word_data.read(self.wordn_max + 1)  #读入wordn_max位
        fp = self.word_data.tell()-1
        i = 1
        while i < self.wordn_max:
            next_word = next_wordmax[0:-i]
            i += 1
            if next_word in self.word_dict:  #如果在词典中找到了
                break  #就退出
        else:  #找不到就滑动一格然后递归调用
            self.word_data.seek(fp - DataInput.__utf8width(next_wordmax, i))
            next_word = self.__next_word()
        self.word_data.seek(fp - DataInput.__utf8width(next_wordmax, i))
        return next_word


    last_word = ''  #记录上一个词


    def __next_batch(self):
        next_word = self.__next_word()  #读入wordn_max位
        batch = (self.last_word, next_word)
        self.last_word = next_word
        return batch


    def next_batchs(self, n):
        batches = []
        for _ in range(0, n):
            batches.append(self.__next_batch())
        return batches
