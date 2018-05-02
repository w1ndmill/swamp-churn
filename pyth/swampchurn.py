# swampchurn
# by slipperyslope
#
# TODO:
# - Chat monitoring
# - Connect monitoring
# - Keyword detection
#

import re
import datetime
import os.path
import sys
from urllib.parse import unquote
from operator import itemgetter

# log file name (optional)
rawLogs = ""

# take input of filename, return list of all log entries
# format: (time, name, steamid, raw log data)
def listify(f, regex = True):
    with open(f, "r", encoding="utf8") as rawFile:
        if regex:
            exp = re.compile(r"\[((?:\d+?.)+)\] (.+)?\((STEAM_0:\d:\d+)\)(.+(?:\n\t.+){0,3})")
            return exp.findall(rawFile.read())

# take input of log entries list, return reformatted list without unwanted entries
def cleanse(unprocessed, retainVideos=True, retainSprays=True, retainChat=False, retainConnects=False):
    processed = []
    vidRegex = re.compile(r"played (video): (.+) \((\w+) \/ (.+)\)")                   # (video, name, source, id)
    sprayRegex = re.compile(r"created (spray): \w+\.(imgur|gfycat).com\/(\w+)\.")      # (spray, source, id)
    # chatRegex = re.compile(r'')
    # connectRegex = re.compile(r'')

    for entry in unprocessed:
        # break tuple and clean up log value
        tim,nam,id,log = entry
        log = unquote(log.replace("\t"," ").replace("\n","").strip())
        bit = log[0]

        # remove all unnecessary values
        if bit in {":","/"}:
            if not retainChat: continue
        elif bit in {"d","s"}:
            if not retainConnects: continue
        elif bit == "p":
            if not retainVideos: continue
            log = vidRegex.match(log)
        elif bit == "c":
            if not retainSprays: continue
            log = sprayRegex.match(log)
        else: continue
        if not log: continue

        processed.append((tim,nam.strip(),id,log.groups()))
    return processed

# takes input of cleansed log entries list, return two sorted lists with duplicate entries and horatio links removed
def fineCleanse(unprocessed, retainHoratio = False):
    videos = []
    videosFinal = []
    sprays = []
    spraysFinal = []

    # seperate into two lists
    for entry in unprocessed:
        if entry[3][0] == "video": videos.append(entry)
        else: sprays.append(entry)

    # sort by video id, then user id for duplication removal
    videos.sort(key=lambda tup: tup[3][3])
    videos.sort(key=lambda tup: tup[2])
    sprays.sort(key=lambda tup: tup[3][2])
    sprays.sort(key=lambda tup: tup[2])

    # if the same person posted the same video, skip over duplicates
    for num in range(len(videos)-1):
        if ((videos[num][2]==videos[num+1][2]) and (videos[num][3][3]==videos[num+1][3][3]) or (videos[num][3][2]=="horatio" and not retainHoratio)):
            continue
        videosFinal.append(videos[num])
    for num in range(len(sprays)-1):
        if (sprays[num][2]==sprays[num+1][2]) and (sprays[num][3][2]==sprays[num+1][3][2]):
            continue
        spraysFinal.append(sprays[num])

    return (videosFinal,spraysFinal)


def riskAnalysis(entry):
    pass

def main():
    print("""
                                           _
             ____ __ ____ _ _ __  _ __  __| |_  _ _ _ _ _ _
            (_-< V  V / _` | '  \| '_ \/ _| ' \| | | '_| ' \\
            /__/\_/\_/\__,_|_|_|_| .__/\__|_||_\_,_|_| |_|_|
                                 |_|
                      version 0.1 -- slipperyslope
    """)

    # get log file correctly
    global rawLogs
    if not rawLogs:
        rawLogs = input("Enter log file name: ")
    while not os.path.isfile(rawLogs):
        rawLogs = input("Error: File \"" + rawLogs + "\" not found\nEnter log file name: ")
    print("Log file \"" + rawLogs + "\" found. Processing...")

    # fetch entries from log file
    logs = listify(rawLogs)
    logLen = len(logs)
    print(logLen,"total entries found")

    # cleanse logs for readibility and get rid of irrelevant stuff
    logs = cleanse(logs)
    print(logLen - len(logs),"entries removed")
    logLen = len(logs)

    # further cleanse logs of duplictes and horatio links
    vidLogs, sprayLogs = fineCleanse(logs)
    print(logLen - (len(vidLogs)+len(sprayLogs)),"duplicates and horatio links removed")

    for vid in vidLogs:
        if(vid[1]=="krubbz"):
            print(vid)
    # for spray in sprayLogs:
    #     print(spray)

    # fetch day for filename
    now = datetime.datetime.now()
    today = str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)

# run this shit
main()
