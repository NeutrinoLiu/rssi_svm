import numpy as np
from common import debug
from sklearn.svm import SVC
import pickle
from config import SVM_KERNEL


class Model():

    def __init__(self):
        self.w = None
        self.b = None
        self.svc = SVC(kernel=SVM_KERNEL)

    def __call__(self, rssi_vector):
        return self.svc.predict([rssi_vector])

    def load(self, weight_file):
        with open(weight_file, "rb") as f:
            self.svc = pickle.load(f)
        # with open(weight_file, "r") as f:
        #     para = json.load(f)
        # self.w = para["weight"]
        # self.b = para["bias"]

    def dump(self, target_file):
        # content = {
        #     "weight" : self.w,
        #     "bias" : self.b
        # }
        # with open(target_file, "w+") as f:
        #     json.dump(content, f, separators=(',', ':'))
        with open(target_file, "wb") as f:
            pickle.dump(self.svc, f)

    def train(self, dataset):
        X = np.array(list(map(lambda pair: pair[0], dataset)))
        y = np.array(list(map(lambda pair: pair[1][0], dataset)))
        debug("shape of input data : {}".format(X.shape))
        debug("shape of label data : {}".format(y.shape))
        self.svc.fit(X,y)
        # debug("support vectors : {}".format(self.svc.support_))
        # self.w = self.svc.coef_.tolist()
        # self.b = self.svc.intercept_.tolist()