from common import getFileStreamer, getRssiStreamer, json2vector
from time import sleep
import config
from time import time


# # file stream test
# streamer = getFileStreamer(config.OFFLINE_FILE)
# # streamer = getRssiStreamer()
# # while True:
# #     st = time()
# #     ret = streamer()
# #     # et = time()
# #     # print(et-st)
# #     print(json2vector(ret))
# #     sleep(1)
# # # 

# print(streamer.extract_dataset())

# from pynput import keyboard

# def on_press(key):
#     if key == keyboard.Key.left:
#         indoor = True
#     if key == keyboard.Key.right:
#         indoor = False

# def on_release(key):
#     if key in keyboard.Key.esc:
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()