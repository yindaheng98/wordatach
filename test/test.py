from wordatas.DataInput import DataInput

data_input = DataInput('斗罗大陆.txt', 10, 10, 0.5)
print(data_input.next_batch(1))
print(data_input.next_batch(1))
print(data_input.next_batch(1))
print(data_input.next_batch(1))
