from common import getFileStreamer, getRssiStreamer, json2vector
from time import sleep
import config
from time import time


# file stream test
streamer = getFileStreamer(config.OFFLINE_FILE)
# streamer = getRssiStreamer()
# while True:
#     st = time()
#     ret = streamer()
#     # et = time()
#     # print(et-st)
#     print(json2vector(ret))
#     sleep(1)
# # 

print(streamer.extract_dataset())