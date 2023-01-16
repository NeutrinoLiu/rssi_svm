import logging as lg
from logging import debug, info, warning, error, critical
import config, subprocess, json

# logging system
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATE_FORMAT = "%H:%M:%S"
lg.basicConfig(level = config.LOGGING, format=LOG_FORMAT, datefmt=DATE_FORMAT)

# wifi rssi streamer
class getFileStreamer():
    def __init__(self, filelist):
        all = []
        for fn in filelist:
            with open(fn, "r") as f:
                jarray = json.load(f)
            all += jarray
        self.alliter = iter(all)
    def __call__(self):
        return next(self.alliter)

def getRssiStreamer(): # pretend to be a class, but just return different function
    if  config.PLATFORM ==  "mac" :
        return rssi_streamer_mac
    else:
        critical("platform not recognized")
        return None

def rssi_streamer_mac(): # return current rssi
    AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    scan_cmd = subprocess.Popen(['sudo', AIRPORT_PATH, '-s'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scan_out, scan_err = scan_cmd.communicate()
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
    return triad_list

# json object to array input

# SVM model definition