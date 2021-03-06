#!/usr/bin/python
# -*- coding:UTF-8 -*-

import numpy as np
import math
from sklearn.externals import joblib
import cPickle
import os
from sklearn.ensemble import RandomForestRegressor
import csv
import time


class OnlineRF:
    # 初始化，神经网络参数，树的数量，数据集路径，训练集与测试集的比例
    def __init__(self, numTrees,input,dataPath='./data/offline/',pct=0.9):
        self.input = input
        self.pct = pct
        self.data = self.get_data(dataPath)
        self.init_data()
        # self.param['xrng'] = dataRange(self.trainX)
        # self.orf = RandomForestRegressor(n_estimators=numTrees,random_state=0)  # 一般来说n_estimators越大越好
        self.orf = RandomForestRegressor()

    def get_data(self,dataPath):
        # 训练的文件全部在data文件夹下，datapath为data的路径，读取该文件夹下的数据文件
        filePath = []
        pathDir = os.listdir(dataPath)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (dataPath, allDir))
            filePath.append(child)
        data = []
        for path in filePath:
            fopen = open(path, 'r')
            for eachLine in fopen:
                eachLineData = eachLine.split(",")
                eachLineData = np.array(map(lambda x:float(x),eachLineData))
                data.append(eachLineData)
            fopen.close()
        return np.array(data)

    # 按照比例分隔数据集，构造训练集和测试集
    def init_data(self):
        self.trainX = self.data[:int(len(self.data)*self.pct),:self.input]
        self.trainY = self.data[:int(len(self.data)*self.pct),self.input:self.input+1]
        self.trainY = np.reshape(self.trainY,[len(self.trainY),])
        self.testX = self.data[int(len(self.data)*self.pct):,:self.input]
        self.testY = self.data[int(len(self.data)*self.pct):,self.input:self.input+1]
        self.testY = np.reshape(self.testY, [len(self.testY),])
        print self.trainX.shape
        print self.trainY.shape

    # 离线训练: EPOCH代表迭代次数（暂时不知道迭代次数是否起作用，默认为1）
    def offline_train(self,EPOCH=1):
        print "train start..."
        for epoch in range(EPOCH):
            self.orf.fit(self.trainX, self.trainY)
            print epoch
        print "train finish!"
        self.save()
        print "save model!"


    # 在线训练: newData代表新产生的data,EPOCH代表迭代次数（暂时不知道迭代次数是否起作用，默认为1），flag为true代表保留旧数据，false代表替换旧数据
    def online_train(self,newDataPath="./data/online/",EPOCH=1,flag=False):
        print "load model..."
        self.load()
        print "Online train start..."
        newData = self.get_data(newDataPath)
        if flag:
            self.data = np.concatenate([self.data,newData],0)
        else:
            self.data = newData
        self.init_data()
        # for ort in self.orf.forest:
        #     ort.tree.elem.xrng = dataRange(self.trainX)
        self.offline_train(EPOCH=1)
        print "Online train finish!"

    def save(self):
        # 保存Model(注:save文件夹要预先建立，否则会报错)
        # joblib.dump(self.orf, "./save/rf.pkl")
        cPickle.dump(self.orf, open("./save/orf.pkl","wb"))

    def load(self):
        # 读取Model
        # self.orf = joblib.load("./save/rf.pkl")
        self.orf = cPickle.load(open("./save/orf.pkl","rb"))

    def test(self,write=True):
        self.load()
        newData = self.get_data("./data/test/")
        self.pct = 0
        self.data = newData
        self.init_data()
        t1 = time.time()
        preds = self.orf.predict(self.testX)
        print "用时："+str(time.time() - t1) + "\n"
        # RMSE 均方根误差亦称标准误差
        # sse = sum(map(lambda z: (z[0] - z[1]) * (z[0] - z[1]), zip(preds, self.testY)))
        # rmse = math.sqrt(sse / float(len(preds)))
        # print "RMSE: " + str(round(rmse, 2)) + "\n"
        if write:
            f = open("./result/orf_result.txt","wb")
            errs = 0
            for i in range(len(preds)):
                err = float((abs(preds[i] - self.testY[i]) / self.testY[i]) * 100)
                errs += err
                line = "预测值：" + str(preds[i]) + " 真实值：" + str(self.testY[i]) + " 误差：" + str(err) + "%"
                print line
                f.writelines(line+"\n")
            line = "平均误差：" + str(errs / len(preds)) + "%"
            print line
            f.writelines(line)
        else:
            errs = 0
            for i in range(len(preds)):
                err = float((abs(preds[i]-self.testY[i])/self.testY[i])*100)
                errs += err
                print "预测值："+str(preds[i])+" 真实值："+str(self.testY[i])+" 误差："+str(err)+"%"
            print "\n 平均误差："+str(errs/len(preds))+"%"
