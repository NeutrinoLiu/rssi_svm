from common import *

print(config.PROJECT_NAME + " - judger")

model = Model() 
model.load(config.PARA_FILE)
info("init SVM model with {}".format(config.PARA_FILE))

info("start wifi scanning, root permission might need")
if config.OFFLINE:
    if len(sys.argv) > 1:
        rssi_reader = getFileStreamer([sys.argv[1]])
    else: rssi_reader = getFileStreamer(config.OFFLINE_FILES)
else: rssi_reader = getRssiStreamer()

II = 0
OO = 0
IO = 0
OI = 0


while True:
    try:
        rssi = rssi_reader()
    except StopIteration:
        break
    if rssi["counter"] == 0:
        continue
    predict = model(json2vector(rssi)[0])
    prob = model.prob(json2vector(rssi)[0])
    pr = predict[0]
    gt = v2s(rssi["indoor"])
    info("{} AP scanned;\tPR:{}\tGT:{}\tconfi:{:.2f} {}".format(rssi["counter"], pr, gt, abs(prob[0][1]-prob[0][0]), "*" if pr != gt else " "))
    if pr == gt == 1:
        II += 1
    elif pr == gt == -1:
        OO += 1
    elif pr == 1:
        OI += 1
    else: IO += 1
    

critical("comprehensive accuracy: {:.4f}".format((II + OO)/(II + OO + IO + OI)))
critical("indoor correctness: {:.4f}, outdoor correctness: {:.4f}".format(II/(II+IO), OO/(OO+OI)))

# a tester
