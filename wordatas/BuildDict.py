#coding=utf-8
import numpy as np
import re



class BuildDict:



    @staticmethod
    def read_origional_file(path):
        '''读取源文件非空字符串'''
        text = []
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f.readlines():
                if zh_pattern.search(line):
                    text.append(line)
        text = np.array(list(''.join(text)))
        return text


    @staticmethod
    def __split_origional_str(text, wordn_max):
        '''原始字符串切分为单字至指定字数的词列表'''
        word_lists = []
        for n in range(wordn_max - 1, 0, -1):
            word_list = []
            for i in range(0, n):
                word_list.append(text[i:i - n])
            word_list = np.array(word_list).transpose().tolist()
            word_list = [''.join(word) for word in word_list]
            word_lists.append(word_list)
        return word_lists


    @staticmethod
    def __count_words(word_lists):
        '''统计单词和对应的词频'''
        word_counts = []
        for word_list in word_lists:
            word_count = {}
            for word in word_list:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            word_counts.append(sorted(word_count.items(), key=lambda x: x[1], reverse=True))
        return word_counts


    @staticmethod
    def build_dict_from_counts(word_counts, feq_min, count_percent):
        '''取出现次数大于min_wordn的前count_percent部分单词构造单词表'''
        word_dict = {}
        for word_count in word_counts:
            middle_count = word_count[int(len([count for count in word_count if count[1] > feq_min]) * count_percent)][
                1]
            for w_c in word_count:
                if w_c[1] > middle_count:
                    word_dict[w_c[0]] = w_c[1]
                else:
                    break
        return word_dict


    @staticmethod
    def count_words(text, wordn_max):  #统计词频
        return BuildDict.__count_words(BuildDict.__split_origional_str(text, wordn_max))


    @staticmethod
    def build_dict(text, wordn_max, feq_min, count_percent):  #构造词典
        return BuildDict.build_dict_from_counts(BuildDict.count_words(text, wordn_max), feq_min, count_percent)
