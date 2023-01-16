import logging as lg
import numpy as np
from logging import debug, info, warning, error, critical
import config, subprocess, json, time


# logging system     ==========================================================================================
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATE_FORMAT = "%H:%M:%S"
lg.basicConfig(level = config.LOGGING, format=LOG_FORMAT, datefmt=DATE_FORMAT)

# wifi rssi streamer ==========================================================================================
class getFileStreamer():
    def __init__(self, filelist):
        self.all = []
        for fn in filelist:
            with open(fn, "r") as f:
                jarray = json.load(f)
            self.all += jarray
        self.alliter = iter(self.all)
    def __call__(self):
        return next(self.alliter)
    def extract_dataset(self):
        return list(map(json2vector, self.all))


def getRssiStreamer(): # pretend to be a class, but just return different function
    if  config.PLATFORM ==  "mac" :
        return rssi_streamer_mac
    else:
        critical("platform not recognized")
        return None

def rssi_streamer_mac(): # return current rssi through airport 
    AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    scan_cmd = subprocess.Popen(['sudo', AIRPORT_PATH, '-s'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scan_out, scan_err = scan_cmd.communicate() # communicate will wait for subprocess exit
    scan_out_lines = str(scan_out).split("\\n")[1:-1]
    triad_list = []
    for l in scan_out_lines:
        # print(l)
        indexOfFirstComma = l.find(":")
        indexOfMAC = indexOfFirstComma - 2
        name = l[:indexOfMAC - 1].strip()
        mac = l[indexOfMAC: indexOfMAC + 17]
        rssi = int(l[indexOfMAC + 18:indexOfMAC + 22])
        triad_list.append([name, mac, rssi])
    triad_list.sort(key = lambda x: x[0])

    # a temporary wrapper to add dummy meta data
    ret = {
        "indoor" : None,
        "location" : "unknown",
        "timestamp" : time.time(),
        "counter" : len(triad_list),
        "fingerprint" : triad_list,
    }

    return ret

# json object to array input =====================================================================================
def apply_filter(triad_list, ap_filter):
    if ap_filter == None:
        return triad_list
    ret_list = []
    for triad in triad_list:
        if triad[1] in ap_filter:
            ret_list.append(triad)
    return ret_list
def json2vector(obj, ap_filter = None, standardization = True):
    if len(obj["fingerprint"]) == 0:
        warning("no fingerprint if fetched")
        return None, None
    fp = apply_filter(obj["fingerprint"], ap_filter)

    if obj["indoor"] == None:
        y = None
    else:
        if obj["indoor"] == 1:
            y = 1
        elif obj["indoor"] == 0:
            y = -1
        else:
            warning("unrecognized indoor label")

    x = [0] * config.RSSI_WIDTH
    # x[0]-AP#ofMIN_RSSI x[-1]-AP#ofMAX_RSSI 
    for triad in fp:
        if triad[2] > config.RSSI_MAX:
            warning("RSSI reading overflow, wrapped")
            idx = -1
        elif triad[2] < config.RSSI_MIN:
            warning("RSSI reading downflow, wrapped")
            idx = 0
        else: 
            idx = triad[2] - config.RSSI_MIN
        x[idx] += 1
    
    x = np.array(x)
    if standardization:
        x = x / np.sum(x)
    # debug(x, y)
    y = np.array([y])
    return x, y

# SVM model definition