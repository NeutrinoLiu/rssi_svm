from logging import DEBUG, INFO, WARNING

PROJECT_NAME = "RSSI BASED BUILDING IN/OUT JUDGER"
MAX_RSSI = -35
MIN_RSSI = -98
LOGGING = DEBUG

PLATFORM = "linux"

OFFLINE_FILE = ["raw/indoor_A.json", "raw/indoor_B.json", "raw/indoor_C.json", "raw/outdoor.json"]
# note "indoor" field in json file: 0-outdoor, 1-indoor, null-noRecord