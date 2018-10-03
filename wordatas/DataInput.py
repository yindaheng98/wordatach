#coding=utf-8
import json
import os

from wordatas.BuildDict import BuildDict



class DataInput:
    dict_size = 0
    word_list = {}  #单词表
    word_dict = {}  #词典
    word_data = ''  #预处理数据文件
    word_hits = []  #各单词的命中次数
    result_path = ''  #结果存储路径
    hit_path = ''


    def __init__(self, path, wordn_max, feq_min, count_percent):
        #数据文件路径
        index_path = path.split('.')[0] + '\\'
        #原文存储路径
        word_data_path = index_path + 'word_data.json'
        #词频存储路径
        word_counts_path = index_path + '字数不大于%d的word_counts.json' % wordn_max
        #单词表存储路径
        word_list_path = index_path + '字数不大于%d且至少出现%d次的词中的前%f%%的word_list.json' % (
            wordn_max, feq_min, count_percent * 100)
        #词典存储路径
        word_dict_path = index_path + '字数不大于%d且至少出现%d次的词中的前%f%%的word_dict.json' % (
            wordn_max, feq_min, count_percent * 100)
        #结果存储路径
        self.result_path = index_path + '字数不大于%d且至少出现%d次的词中的前%f%%%%' % (
            wordn_max, feq_min, count_percent * 100) + '的%d维词向量.json'
        self.hit_path = index_path + '字数不大于%d且至少出现%d次的词中的前%f%%的命中次数.json' % (
            wordn_max, feq_min, count_percent * 100)
        #读取原文
        if not os.path.exists(index_path):
            os.makedirs(index_path)  #没有路径先创建路径
        #读取或构建词典
        if os.path.exists(word_dict_path):  #如果有词典文件存在
            print('词典文件存在')
            with open(word_dict_path, 'r', encoding='utf-8') as f:  #就直接读取树形词典
                word_dict = json.load(f)
                print('词典文件已读取')
        else:
            print('词典文件不存在')
            if os.path.exists(word_list_path):  #如果有单词表文件存在
                print('单词表文件存在')
                with open(word_list_path, 'r', encoding='utf-8') as f:  #就直接读取单词表
                    word_list = json.load(f)
                    print('单词表文件已读取')
            else:  #如果没有单词表文件
                print('单词表文件不存在')
                if os.path.exists(word_counts_path):  #但有词频文件
                    print('词频文件存在')
                    with open(word_counts_path, 'r', encoding='utf-8') as f:  #就直接读取词频
                        word_counts = json.load(f)
                        print('词频文件已读取')
                else:  #如果没有词频文件
                    print('词频文件不存在')
                    if os.path.exists(word_data_path):  #但有预处理数据文件
                        print('预处理数据文件存在')
                        word_data = BuildDict.read_origional_file(word_data_path)  #就读取预处理数据文件
                        print('预处理数据已读取')
                    else:
                        print('预处理数据文件不存在')
                        word_data = BuildDict.read_origional_file(path)  #构建预处理数据
                        with open(word_data_path, 'w', encoding='utf-8') as f:  #记录预处理数据文件
                            f.writelines(word_data)
                            print('预处理数据文件已构建')
                    word_counts = BuildDict.count_words(word_data, wordn_max)  #构建词频
                    with open(word_counts_path, 'w', encoding='utf-8') as f:  #记录词频文件
                        json.dump(word_counts, f)
                        print('词频文件已构建')
                word_list = BuildDict.build_list_from_counts(word_counts, feq_min, count_percent)  #构建单词表
                with open(word_list_path, 'w', encoding='utf-8') as f:  #记录单词表文件
                    json.dump(word_list, f)
                    print('单词表文件已构建')
            word_dict = BuildDict.build_dict_from_list(word_list)  #构建词典
            with open(word_dict_path, 'w', encoding='utf-8') as f:  #记录词典文件
                json.dump(word_dict, f)
                print('词典文件已构建')
        self.word_dict = word_dict
        print('词典初始化完成')
        with open(word_list_path, 'r', encoding='utf-8') as f:  #记录词典文件
            self.word_list = json.load(f)  #单词表文件进入内存
        print('单词表初始化完成')
        self.word_data = open(word_data_path, 'r', encoding='utf-8')  #打开原数据文件
        print('预处理数据初始化完成')
        self.dict_size = len(self.word_list)
        print('单词表大小%d' % self.dict_size)
        self.word_hits = [0] * self.dict_size
        self.wordn_max = wordn_max
        self.words = []
        self.__update_words()
        self.last_word = self.__next_word()
        self.this_word = self.__next_word()


    def data_reload(self, word_data_path):
        """重新载入数据文件,用于在生成词典之后切换其他源文件"""
        self.word_data.close()
        self.word_data = open(word_data_path, 'r', encoding='utf-8')  #打开原数据文件
        print('预处理数据源%s切换完成' % word_data_path)
        self.words = []
        self.__update_words()
        self.last_word = self.__next_word()
        self.this_word = self.__next_word()
        self.words = []


    def data_reload_current(self):
        """重新载入当前的数据文件"""
        self.word_data.seek(0)
        self.words = []


    wordn_max = 0  #最大子长
    words = []  #要检测的一串字


    def __update_words(self):
        """更新last_w使长度达到wordn_max字"""
        needs = self.wordn_max - len(self.words)  #算出缺少多少字达到wordn_max字
        for _ in range(0, needs):
            self.words.append(self.word_data.read(1))  #并读入一串字
        if self.words[-1] == '':
            raise IOError('文件已读完')


    def __next_word(self):
        """从文本中切出一个单词"""
        self.__update_words()  #先补齐words
        has_id = []
        next_word = 0
        r = self.word_dict  #开始树形搜索,r表示树形搜索当前到达的范围
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
                    r = self.word_dict
                    for j in range(0, layer):
                        r = r[self.words[j]]
                    next_word = r['id']  #返回最近的有id词语
                    self.words = self.words[layer if not layer == 0 else 1:]  #然后把已检索到的词删掉
                break
        self.word_hits[next_word] += 1  #记录命中次数
        return next_word


    last_word = ''  #记录前一个词
    this_word = ''  #记录中间的词


    def __next_batch(self):
        """下一个训练对"""
        while 1:
            next_word = self.__next_word()  #记录下一个词
            batch = ([self.last_word, next_word], self.this_word)
            self.last_word = self.this_word
            self.this_word = next_word
            if (0 not in batch) and (0 not in batch[0]):
                break  #找到一个全不为0的batch才退出
        return batch


    def next_batches_for_cbow(self, n):
        """读出n个训练对,为CBOW模型"""
        batches = []
        for _ in range(0, n):
            batches.append(self.__next_batch())
        return batches


    def next_batches_for_skipgram(self, n):
        """读出n个训练对,为SkipGram模型"""
        batches = []
        while len(batches) < n:
            batch = self.__next_batch()
            batches.append((batch[1], batch[0][0]))
            batches.append((batch[1], batch[0][1]))
        return batches


    def record_result(self, word_vec_list):
        """记录词向量结果"""
        with open(self.result_path % (len(word_vec_list[0])), 'w') as f:
            json.dump({'word_list': self.word_list, 'word_vec_list': word_vec_list, 'word_hits': self.word_hits}, f)
        print('结果及各单词命中次数已写入%s' % self.result_path)
