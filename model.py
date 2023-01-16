import json, config
import numpy as np

class Model():
    def __init__(self):
        self.w = [.0] * (config.RSSI_WIDTH)
        self.b = [.0] * (config.RSSI_WIDTH)
    def __call__(self, input):
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