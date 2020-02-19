#!/usr/bin/python
# -*- coding:UTF-8 -*-

from models.ORF import OnlineRF
from models.OKNN import OnlineKNN
from models.OSVR import OnlineSVR
from models.OLR import OnlineLR
from models.OMLP import OnlineMLP
import warnings
warnings.filterwarnings("ignore")


if __name__ == "__main__":
    # 选择模型的类型：orf、oknn、osvr、olr、omlp
    model = "omlp"

    if model == "orf":
        orf = OnlineRF(numTrees=100,input=722,pct=1)
        orf.offline_train()
        orf.online_train()
        orf.test()
    elif model == "oknn":
        oknn = OnlineKNN(input=722,pct=1)
        oknn.offline_train()
        oknn.online_train()
        oknn.test()
    elif model == "osvr":
        osvr = OnlineSVR(input=722,pct=1)
        osvr.offline_train()
        osvr.online_train()
        osvr.test()
    elif model == "olr":
        olr = OnlineLR(input=722,pct=1)
        olr.offline_train()
        olr.online_train()
        olr.test()
    elif model == "omlp":
        omlp = OnlineMLP(input=722,pct=1)
        omlp.offline_train()
        omlp.online_train()
        omlp.test()
