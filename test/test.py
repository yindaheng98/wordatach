from wordatas.DataInput import DataInput
import numpy as np

data_input = DataInput('斗罗大陆.txt', 10, 10, 0.5)
print(data_input.next_batches_for_cbow(32))
print(data_input.next_batches_for_cbow(30))
print(data_input.next_batches_for_cbow(10))
print(data_input.next_batches_for_cbow(10))
print(data_input.next_batches_for_skipgram(32))
print(data_input.next_batches_for_skipgram(30))
print(data_input.next_batches_for_skipgram(10))
print(data_input.next_batches_for_skipgram(10))

batches = data_input.next_batches_for_skipgram(10)
batches=np.array(batches)
inputs=batches[:,0].reshape(1,-1)
outputs=batches[:,1]
data_input.word_data.close()

'''
#Here is the bug,watch the variable t and see what will happen
f = open('斗罗大陆/word_data.json', 'r', encoding='utf-8')
while 1:
    f.seek(34)
    fp=f.tell()
    t=f.read(11)
    fp=f.tell()
    fp
f = open('斗罗大陆/word_data.json', 'r', encoding='utf-8')
while 1:
    f.seek(0)
    fp=f.tell()
    t=f.read(12)
    fp=f.tell()
    t = f.seek(18446744073709551650)
    t = f.read(12)
    fp
'''