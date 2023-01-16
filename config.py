from logging import DEBUG, INFO, WARNING

PROJECT_NAME = "RSSI BASED BUILDING IN/OUT JUDGER"
RSSI_MAX = -30
RSSI_MIN = -99
RSSI_WIDTH = RSSI_MAX - RSSI_MIN + 1
LOGGING = DEBUG

PARA_FILE = "svm_weight.json"

PLATFORM = "mac"
# PLATFORM = "win"
# PLATFORM = "linux"

JUDGER_SLEEP = 1

OFFLINE_FILE = ["raw/indoor_A.json", "raw/indoor_B.json", "raw/indoor_C.json", "raw/outdoor.json"]
# note "indoor" field in json file: 0-outdoor, 1-indoor, null-noRecord