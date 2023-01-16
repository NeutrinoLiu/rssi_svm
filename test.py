from common import getFileStreamer, getRssiStreamer
from time import sleep
import config


# file stream test
streamer = getFileStreamer(config.OFFLINE_FILE)
while True:
    print(streamer())
    sleep(1)
