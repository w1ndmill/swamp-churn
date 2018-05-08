# swampchurn
# by slipperyslope
#
# TODO:
# - Chat monitoring
# - Connect monitoring
# - Keyword detection
# - rad

from logClasses import *
import os.path
import click

# log file name (optional)
rawLogs = ""

def main():
    global rawLogs

    if not rawLogs:
        rawLogs = input("Enter log file name: ")
    while not os.path.isfile(rawLogs):
        rawLogs = input("Error: File \"" + rawLogs + "\" not found\nEnter log file name: ")
    print("Log file \"" + rawLogs + "\" found. Processing...")

    logs = swampLogs(rawLogs)
    logs.build()
    videos, sprays = logs.getLists("video","spray")
    for video in videos:
        print(video)

if __name__ == "__main__":
    main()
