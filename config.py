from logging import DEBUG, INFO, WARNING, CRITICAL

OFFLINE = True

SVM_KERNEL = 'rbf'

PROJECT_NAME = "RSSI BASED INDOOR/OUTDOOR JUDGER"
RSSI_MAX = -23
RSSI_MIN = -99
RSSI_WIDTH = RSSI_MAX - RSSI_MIN + 1
LOGGING = CRITICAL

PARA_FILE = "svm_weight.pickle"

PLATFORM = "mac"
# PLATFORM = "win"
# PLATFORM = "linux"

OFFLINE_FILES = ["raw/indoor_A.json", "raw/indoor_B.json", "raw/indoor_C.json", "raw/outdoor.json"]
# note "indoor" field in json file: 0-outdoor, 1-indoor, null-noRecord