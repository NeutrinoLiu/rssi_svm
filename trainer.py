# -*- coding: utf-8 -*-

from common import *
import datetime
from pynput import keyboard

print(config.PROJECT_NAME + " - trainer component")

# 1 record rssi data and manual labeling
# 2 perform svm training
# 3 stores to svm_weight.json

info("step 1 - training set sampling") # =============================================

indent = "                "
label = input(indent + "are you currently indoor (y/n) ? ").capitalize()
while label not in ["Y", "N", "YES", "NO"]:
    print(indent + "unrecognized answer")
    label = input(indent + "are you currently indoor (y/n) ? ").capitalize()
if label in ["Y", "YES"]:
    indoor = True
else:
    indoor = False

info("current label is {}".format(b2s(indoor)))
print(indent + "switch by [← indoor, → outdoor], finish by [ESC]")
info("start wifi scanning, root permission might need")
rssi_reader = getRssiStreamer()
sample = rssi_reader()

term_flag = False
indoor = indoor

# keyboard reader =========================================
def on_press(key):
    global indoor
    if key == keyboard.Key.left:
        indoor = True
        info("now labeled as {}".format(b2s(indoor)))
    if key == keyboard.Key.right:
        indoor = False
        info("now labeled as {}".format(b2s(indoor)))

def on_release(key):
    global term_flag
    if key == keyboard.Key.esc:
        term_flag = True
        info("finishing the last sampling")
        return False

# Collect events until released
listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
listener.start()
# eof keyboard reader =====================================

record = []
try:
    while not term_flag:
        # debug(sample)
        if sample["counter"] == 0:
            sample = rssi_reader()
            continue
        sample["indoor"] = b2v(indoor)
        record.append(sample)
        info("{} AP scanned; labeled as {}".format(sample["counter"], b2s(indoor)) + 
        "; press ESC to finish")
        sample = rssi_reader()
except KeyboardInterrupt:
    info("keyboard interrupt detected")
    listener.stop()

target_file = "log/record_{}.json".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
with open(target_file, "w+") as f:
    json.dump(record, f, indent = 1)
info("training set stored to {}, {} records in total".format(target_file, len(record)))

info("step 2 - train SVM with dataset") # =============================================
model = Model()
dataset = list(map(json2vector, record)) 
# [ (x, y),
#   (x, y) ]
model.train(dataset)

model.dump(config.PARA_FILE)
info("step 3 - trained SVM model has been saved to {}".format(config.PARA_FILE)) # ====
print(indent + "plz run judger with trained model")


