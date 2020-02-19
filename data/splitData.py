#!/usr/bin/python
# -*- coding:UTF-8 -*-

import numpy as np
import csv
import random

# 读取全部的数据
fopen = open("./data.csv", 'r')
tempData = []
for eachLine in fopen:
    eachLineData = eachLine.split(",")
    eachLineData[-1] = str(float(eachLineData[-1]))
    tempData.append(eachLineData)
fopen.close()

# 把数据分开，保存在三个文件夹下
fopenOffline = open("./offline/data.csv","wb")
fopenOnline = open("./online/data.csv","wb")
fopenTest = open("./test/data.csv","wb")

# 打乱顺序
random.shuffle(tempData)

#比例为 0.6  0.3  0.1
offlineData = []
onlineData = []
testData = []

a = int(len(tempData)*0.6)
b = int(len(tempData)*0.9)

for i in range(0,a):
    offlineData.append(tempData[i])

for i in range(a,b):
    onlineData.append(tempData[i])

for i in range(b,len(tempData)):
    testData.append(tempData[i])

csv_writer = csv.writer(fopenOffline)
for i in offlineData:
    csv_writer.writerow(i)
fopenOffline.close()

csv_writer = csv.writer(fopenOnline)
for i in onlineData:
    csv_writer.writerow(i)
fopenOnline.close()

csv_writer = csv.writer(fopenTest)
for i in testData:
    csv_writer.writerow(i)
fopenTest.close()
