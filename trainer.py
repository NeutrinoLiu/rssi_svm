# -*- coding: utf-8 -*-

from common import *
import datetime
from pynput import keyboard


print(config.PROJECT_NAME + " - trainer")
INDENT = "                "

if config.OFFLINE:
    if len(sys.argv) > 1:
        rssi_reader = getFileStreamer([sys.argv[1]])
    else: rssi_reader = getFileStreamer(config.OFFLINE_FILES)
else: rssi_reader = getRssiStreamer()

# 1 record rssi data and manual labeling
# 2 perform svm training
# 3 stores to svm_weight.json

info("[step 1] sample training dataset") # =============================================

if not config.OFFLINE: # online mode, need to init with current label
    ans = input(INDENT + "are you currently indoor (y/n) ? ").capitalize()
    while ans not in ["Y", "N", "YES", "NO"]:
        print(INDENT + "unrecognized answer")
        ans = input(INDENT + "are you currently indoor (y/n) ? ").capitalize()
    if ans in ["Y", "YES"]:
        indoor = True
    else:
        indoor = False
else:
    indoor = False

info("init label as {}".format(b2s(indoor)))
print(INDENT + "switch by [← indoor, → outdoor], finish by [ESC]")
info("start wifi scanning, root permission might need")
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
        if sample["indoor"] == None:
            sample["indoor"] = b2v(indoor)
        record.append(sample)
        info("{} AP scanned; labeled as {}".format(sample["counter"], b2s(sample["indoor"])) + 
        "; press ESC to finish")
        sample = rssi_reader()
except (KeyboardInterrupt, StopIteration):
    info("Interrupt detected")
    listener.stop()

target_file = "log/record_{}.json".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
with open(target_file, "w+") as f:
    json.dump(record, f, indent = 1)
info("training set stored to {}, {} records in total".format(target_file, len(record)))

info("[step 2] train SVM with dataset") # =============================================
model = Model()
dataset = list(map(json2vector, record)) 
# [ (x, y),
#   (x, y) ]
model.train(dataset)

model.dump(config.PARA_FILE)
info("[step 3] save trained SVM model to {}".format(config.PARA_FILE)) # ====
print(INDENT + "plz run judger with trained model")


