from common import *
from model import Model

print(config.PROJECT_NAME + " - judger component")

rssi_reader = getRssiStreamer()

model = Model()
model.load(config.PARA_FILE)
while True:
    rssi = rssi_reader()
    if rssi["counter"] == 0:
        continue
    predict = model(json2vector(rssi)[0])
    info("{} AP scanned; chances of indoor to be {}".format(rssi["counter"], predict.tolist()))

# a tester
