import json, config
import numpy as np
from common import debug
from sklearn.svm import SVC


class Model():

    def __init__(self):
        self.w = None
        self.b = None

    def __call__(self, rssi_vector):
        return np.array([1.0])

    def load(self, weight_file):
        with open(weight_file, "r") as f:
            para = json.load(f)
        self.w = para["weight"]
        self.b = para["bias"]

    def dump(self, target_file):
        content = {
            "weight" : self.w,
            "bias" : self.b
        }
        with open(target_file, "w+") as f:
            json.dump(content, f, separators=(',', ':'))

    def train(self, dataset):
        X = np.array(list(map(lambda pair: pair[0], dataset)))
        y = np.array(list(map(lambda pair: pair[1][0], dataset)))
        debug("shape of input data : {}".format(X.shape))
        debug("shape of label data : {}".format(y.shape))
        svc = SVC(kernel = "linear", C = 1)
        svc.fit(X,y)
        self.w = svc.coef_.tolist()
        self.b = svc.intercept_.tolist()