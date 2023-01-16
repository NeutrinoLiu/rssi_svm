from common import *

print(config.PROJECT_NAME + " - judger")

model = Model() 
model.load(config.PARA_FILE)
info("init SVM model with {}".format(config.PARA_FILE))

info("start wifi scanning, root permission might need")
if config.OFFLINE:
    rssi_reader = getFileStreamer(config.OFFLINE_FILE)
else: rssi_reader = getRssiStreamer()

while True:
    rssi = rssi_reader()
    if rssi["counter"] == 0:
        continue
    predict = model(json2vector(rssi)[0])
    info("{} AP scanned; chances of being indoor is {}".format(rssi["counter"], predict.tolist()[0]))
    time.sleep(config.JUDGER_SLEEP)

# a tester
