# -*- coding: utf-8 -*-

import numpy as np
np.random.seed(1337)  
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt

def load_data(filename, seq_len, normalise_window):
    f = open(filename).read()
    data = f.split('\n')

    print('data len:',len(data))
    print('sequence len:',seq_len)

    sequence_length = seq_len + 1
    result = []
    for item in data:
        result.append(data.split(",")[1:])  #得到长度为seq_len+1的向量，最后一个作为label

    print('result len:',len(result))
    print('result shape:',np.array(result).shape)
    print(result[:1])

    if normalise_window:
        result = normalise_windows(result)

    print(result[:1])
    print('normalise_windows result shape:',np.array(result).shape)

    result = np.array(result)

    #划分train、test
    row = round(0.9 * result.shape[0])
    train = result[:row, :]
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = result[row:, :-1]
    y_test = result[row:, -1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return [x_train, y_train, x_test, y_test]

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:   #window shape (sequence_length L ,)  即(51L,)
        #normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        normalised_window.append(float(window[0])/float(41))
        normalised_window.append(float(window[1])/float(3210))
        normalised_window.append(float(window[2])/float(28))
        normalised_window.append(float(window[3])/float(3210))
        normalised_data.append(normalised_window)
    return normalised_data

# 生成数据
#X = np.linspace(-1, 1, 200) #在返回（-1, 1）范围内的等差序列
#np.random.shuffle(X)    # 打乱顺序
#Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200, )) #生成Y并添加噪声
# plot
#plt.scatter(X, Y)
#plt.show()

#X_train, Y_train = X[:160], Y[:160]     # 前160组数据为训练数据集
#X_test, Y_test = X[160:], Y[160:]      #后40组数据为测试数据集

X_train, Y_train, X_test, Y_test = load_data(filename='price.csv',seq_len=0,normalise_window=true)

# 构建神经网络模型
model = Sequential()
model.add(Dense(input_dim=3, units=1))

# 选定loss函数和优化器
model.compile(loss='mse', optimizer='sgd')

# 训练过程
print('Training -----------')
for step in range(501):
    cost = model.train_on_batch(X_train, Y_train)
    if step % 50 == 0:
        print("After %d trainings, the cost: %f" % (step, cost))

# 测试过程
print('\nTesting ------------')
cost = model.evaluate(X_test, Y_test, batch_size=40)
print('test cost:', cost)
W, b = model.layers[0].get_weights()
print('Weights=', W, '\nbiases=', b)

# 将训练结果绘出
Y_pred = model.predict(X_test)
plt.scatter(X_test, Y_test)
plt.plot(X_test, Y_pred)
plt.show()